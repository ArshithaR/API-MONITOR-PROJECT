"""Flask Routes for API Monitor"""
import csv
import json
from io import StringIO, BytesIO
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, Response, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, API, Log, HealthScore, Alert, Notification
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from app.analytics import calculate_health_score, get_analytics_data, get_status_distribution, predict_downtime
from app.alerts import create_alert, get_unread_alerts, mark_alert_as_read, check_api_health

# Initialize Blueprint
main = Blueprint('main', __name__)

# --- 1. AUTHENTICATION ROUTES ---

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email', '')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('main.register'))
            
        new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# --- 2. DASHBOARD & MANAGEMENT ---

@main.route('/dashboard')
@login_required
def dashboard():
    user_apis = API.query.filter_by(user_id=current_user.id).all()
    api_status_dict = {}
    total_up = 0
    total_down = 0
    
    for api in user_apis:
        last_log = Log.query.filter_by(api_id=api.id).order_by(Log.timestamp.desc()).first()
        health = HealthScore.query.filter_by(api_id=api.id).first()
        
        if last_log:
            is_active = last_log.status_code == 200
            status = "🟢 Active" if is_active else "🔴 Down"
            if is_active:
                total_up += 1
            else:
                total_down += 1
        else:
            status = '🟡 Pending'
        
        health_score = health.health_score if health else 100
        health_status = health.status if health else 'excellent'
        
        api_status_dict[api.id] = {
            'status': status,
            'last_checked': last_log.timestamp if last_log else 'N/A',
            'response_time': last_log.response_time if last_log else 'N/A',
            'health_score': health_score,
            'health_status': health_status
        }
    
    unread_alerts = get_unread_alerts(current_user.id)
    
    return render_template('dashboard.html', 
                         apis=user_apis,
                         api_status=api_status_dict,
                         total_up=total_up,
                         total_down=total_down,
                         unread_alerts=len(unread_alerts))

@main.route('/add_api', methods=['POST'])
@login_required
def add_api():
    name = request.form.get('name')
    url = request.form.get('url')
    interval = request.form.get('interval', 300, type=int)
    threshold = request.form.get('threshold', 1000, type=int)
    
    if name and url:
        new_api = API(name=name, url=url, user_id=current_user.id, interval=interval, threshold_latency=threshold)
        db.session.add(new_api)
        db.session.commit()
        flash(f'API "{name}" added successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/delete_api/<int:id>', methods=['POST'])
@login_required
def delete_api(id):
    api = API.query.get_or_404(id)
    if api.user_id == current_user.id:
        api_name = api.name
        Log.query.filter_by(api_id=id).delete()
        HealthScore.query.filter_by(api_id=id).delete()
        Alert.query.filter_by(api_id=id).delete()
        db.session.delete(api)
        db.session.commit()
        flash(f'API "{api_name}" removed successfully!', 'success')
    return redirect(url_for('main.dashboard'))

# --- 3. PERFORMANCE & ANALYTICS ROUTES ---

@main.route('/performance')
@login_required
def performance():
    user_apis = API.query.filter_by(user_id=current_user.id).all()
    return render_template('performance.html', apis=user_apis)

@main.route('/api/analytics/<int:api_id>')
@login_required
def get_analytics(api_id):
    """API endpoint for analytics data"""
    api = API.query.get_or_404(api_id)
    if api.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    time_range = request.args.get('range', 24, type=int)
    data = get_analytics_data(api_id, time_range)
    
    return jsonify({
        'api_name': api.name,
        'total_requests': data['total_requests'],
        'success_count': data['success_count'],
        'failure_count': data['failure_count'],
        'success_rate': round(data['success_rate'], 2),
        'avg_response_time': round(data['avg_response_time'], 2),
        'min_response_time': round(data['min_response_time'], 2),
        'max_response_time': round(data['max_response_time'], 2),
    })

@main.route('/api/chart-data/<int:api_id>')
@login_required
def get_chart_data(api_id):
    """Get chart data for visualization"""
    api = API.query.get_or_404(api_id)
    if api.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    chart_type = request.args.get('type', 'line')
    time_range = request.args.get('range', 24, type=int)
    
    logs = Log.query.filter_by(api_id=api_id).filter(
        Log.timestamp >= datetime.utcnow() - timedelta(hours=time_range)
    ).order_by(Log.timestamp.asc()).all()
    
    if chart_type in ['line', 'area', 'bar']:
        return jsonify({
            'type': chart_type,
            'labels': [l.timestamp.strftime('%H:%M') for l in logs],
            'datasets': [{
                'label': 'Response Time (ms)',
                'data': [l.response_time for l in logs],
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.1)',
                'fill': chart_type == 'area'
            }]
        })
    
    elif chart_type == 'pie':
        status_dist = get_status_distribution(api_id, time_range)
        return jsonify({
            'type': 'pie',
            'labels': [f'Status {k}' for k in status_dist.keys()],
            'datasets': [{
                'data': list(status_dist.values()),
                'backgroundColor': ['#4CAF50', '#FF9800', '#F44336', '#2196F3']
            }]
        })
    
    return jsonify({'error': 'Invalid chart type'}), 400

@main.route('/api/health/<int:api_id>')
@login_required
def get_health(api_id):
    """Get API health score"""
    api = API.query.get_or_404(api_id)
    if api.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    health = HealthScore.query.filter_by(api_id=api_id).first()
    if not health:
        return jsonify({'error': 'Health data not available'}), 404
    
    # Get status badge
    if health.status == 'excellent':
        status_badge = '🟢 Excellent'
    elif health.status == 'good':
        status_badge = '🟡 Good'
    else:
        status_badge = '🔴 Poor'
    
    return jsonify({
        'health_score': round(health.health_score, 2),
        'status': health.status,
        'status_badge': status_badge,
        'uptime': round(health.uptime_percentage, 2),
        'avg_response_time': round(health.avg_response_time, 2),
        'success_rate': round(health.success_rate, 2),
        'updated_at': health.updated_at.isoformat()
    })

@main.route('/api/prediction/<int:api_id>')
@login_required
def get_prediction(api_id):
    """Get downtime prediction"""
    api = API.query.get_or_404(api_id)
    if api.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    prediction = predict_downtime(api_id)
    return jsonify(prediction)

# --- 4. ALERTS & NOTIFICATIONS ---

@main.route('/alerts')
@login_required
def alerts():
    user_alerts = Alert.query.filter_by(user_id=current_user.id).order_by(Alert.created_at.desc()).limit(50).all()
    return render_template('alerts.html', alerts=user_alerts)

@main.route('/api/alerts/unread')
@login_required
def get_unread_alerts_api():
    """Get unread alerts count"""
    count = Alert.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'unread_count': count})

@main.route('/alert/<int:alert_id>/read', methods=['POST'])
@login_required
def read_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    if alert.user_id == current_user.id:
        mark_alert_as_read(alert_id)
        return jsonify({'success': True})
    return jsonify({'error': 'Unauthorized'}), 403

# --- 5. EXPORT ROUTES ---

@main.route('/export/csv')
@login_required
def export_csv():
    api_id = request.args.get('api_id')
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['API Name', 'URL', 'Status Code', 'Response Time (ms)', 'Timestamp'])

    if api_id:
        api = API.query.get_or_404(api_id)
        if api.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        apis = [api]
    else:
        apis = API.query.filter_by(user_id=current_user.id).all()

    for api in apis:
        logs = Log.query.filter_by(api_id=api.id).order_by(Log.timestamp.desc()).all()
        for log in logs:
            cw.writerow([api.name, api.url, log.status_code, log.response_time, log.timestamp])

    output = si.getvalue()
    return Response(output, mimetype="text/csv", 
                   headers={"Content-disposition": "attachment; filename=api_monitor_report.csv"})

# --- 6. COMPARISON ROUTES ---

@main.route('/compare')
@login_required
def compare_apis():
    """Compare multiple APIs"""
    user_apis = API.query.filter_by(user_id=current_user.id).all()
    return render_template('compare.html', apis=user_apis)

@main.route('/api/compare', methods=['POST'])
@login_required
def api_compare():
    """Get comparison data for multiple APIs"""
    api_ids = request.json.get('api_ids', [])
    
    comparison_data = []
    for api_id in api_ids:
        api = API.query.get(api_id)
        if not api or api.user_id != current_user.id:
            continue
        
        health = HealthScore.query.filter_by(api_id=api_id).first()
        logs = Log.query.filter_by(api_id=api_id).order_by(Log.timestamp.asc()).all()
        
        comparison_data.append({
            'name': api.name,
            'url': api.url,
            'health_score': health.health_score if health else 0,
            'timestamps': [l.timestamp.isoformat() for l in logs],
            'response_times': [l.response_time for l in logs]
        })
    
    return jsonify(comparison_data)

# --- 7. SETTINGS & MANAGEMENT ---

@main.route('/settings')
@login_required
def settings():
    user_apis = API.query.filter_by(user_id=current_user.id).all()
    return render_template('settings.html', apis=user_apis)

@main.route('/api/<int:api_id>/settings', methods=['POST'])
@login_required
def update_api_settings(api_id):
    api = API.query.get_or_404(api_id)
    if api.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    api.interval = request.json.get('interval', api.interval)
    api.threshold_latency = request.json.get('threshold', api.threshold_latency)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Settings for "{api.name}" updated'})

# --- 8. STATUS PAGE ---

@main.route('/status')
def status():
    """Public status page"""
    users_count = User.query.count()
    apis_count = API.query.count()
    logs_count = Log.query.count()
    
    return render_template('status.html', 
                          users_count=users_count,
                          apis_count=apis_count, 
                          logs_count=logs_count)

# Legacy routes for backwards compatibility
@main.route('/csv_page')
@login_required
def csv_page():
    return redirect(url_for('main.export_csv'))

@main.route('/manage')
@login_required
def manage():
    return redirect(url_for('main.settings'))

@main.route('/charts')
@login_required
def charts():
    return redirect(url_for('main.performance'))