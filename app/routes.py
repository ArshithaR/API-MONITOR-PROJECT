from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, API, APILog
from datetime import datetime, timedelta
import csv
from io import StringIO, BytesIO
import requests

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)

# ==================== AUTHENTICATION ====================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# ==================== MAIN PAGES ====================

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    apis = API.query.filter_by(user_id=current_user.id).all()
    api_data = []
    
    for api in apis:
        log = api.get_last_log()
        avg_response = api.get_avg_response_time()
        
        # Determine status more accurately
        if not log:
            status = '⏳ Pending'
            status_class = 'warning'
        elif log.status_code == 200:
            status = '✅ Active'
            status_class = 'success'
        else:
            status = '❌ Down'
            status_class = 'danger'
        
        api_data.append({
            'id': api.id,
            'name': api.name,
            'url': api.url,
            'status': status,
            'status_class': status_class,
            'response_time': f"{log.response_time:.0f}ms" if log and log.response_time else 'N/A',
            'avg_response_time': f"{avg_response:.0f}ms" if avg_response > 0 else 'N/A',
            'last_checked': log.timestamp.strftime('%Y-%m-%d %H:%M:%S') if log else 'Never',
            'status_code': log.status_code if log else 'N/A'
        })
    
    return render_template('dashboard.html', apis=api_data)

@main_bp.route('/analytics')
@login_required
def analytics():
    apis = API.query.filter_by(user_id=current_user.id).all()
    return render_template('analytics.html', apis=apis)

@main_bp.route('/alerts')
@login_required
def alerts():
    return render_template('alerts.html')

@main_bp.route('/csv')
@login_required
def csv_page():
    """Display CSV data in a table"""
    apis = API.query.filter_by(user_id=current_user.id).all()
    csv_data = []
    
    for api in apis:
        logs = APILog.query.filter_by(api_id=api.id).order_by(APILog.timestamp.desc()).limit(100).all()
        for log in logs:
            csv_data.append({
                'api_name': api.name,
                'url': api.url,
                'status_code': log.status_code or 'N/A',
                'response_time': f"{log.response_time:.0f}ms" if log.response_time else 'N/A',
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'status': '✅ Success' if log.status_code == 200 else '❌ Failed'
            })
    
    return render_template('csv_data.html', csv_data=csv_data, total=len(csv_data))

@main_bp.route('/export-csv')
@login_required
def export_csv():
    apis = API.query.filter_by(user_id=current_user.id).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['API Name', 'URL', 'Status Code', 'Response Time (ms)', 'Timestamp'])
    
    for api in apis:
        logs = APILog.query.filter_by(api_id=api.id).order_by(APILog.timestamp.desc()).limit(100).all()
        for log in logs:
            writer.writerow([
                api.name,
                api.url,
                log.status_code or 'N/A',
                log.response_time or 'N/A',
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
    
    return output.getvalue(), 200, {'Content-Disposition': 'attachment; filename=api_monitor.csv', 'Content-Type': 'text/csv'}

# ==================== API ENDPOINTS ====================

@main_bp.route('/api/add', methods=['POST'])
@login_required
def add_api():
    name = request.form.get('name')
    url = request.form.get('url')
    interval = request.form.get('interval', 60, type=int)
    
    api = API(name=name, url=url, user_id=current_user.id, interval=interval)
    db.session.add(api)
    db.session.commit()
    
    flash(f'API "{name}" added successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/api/delete/<int:api_id>', methods=['POST'])
@login_required
def delete_api(api_id):
    api = API.query.get_or_404(api_id)
    if api.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(api)
    db.session.commit()
    flash('API deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/api/chart-data/<int:api_id>')
@login_required
def get_chart_data(api_id):
    """Get chart data for graphs with support for multiple chart types"""
    api = API.query.get_or_404(api_id)
    if api.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    hours = request.args.get('hours', 24, type=int)
    chart_type = request.args.get('type', 'line')  # line, bar, pie, area
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    
    logs = APILog.query.filter(
        APILog.api_id == api_id,
        APILog.timestamp >= cutoff
    ).order_by(APILog.timestamp.asc()).all()
    
    if not logs:
        return jsonify({
            'labels': [],
            'response_times': [],
            'status_codes': [],
            'timestamps': [],
            'chart_type': chart_type
        })
    
    # Prepare data based on chart type
    if chart_type == 'pie' or chart_type == 'doughnut':
        # For pie/doughnut: aggregate by status
        success = len([l for l in logs if l.status_code == 200])
        failed = len(logs) - success
        return jsonify({
            'labels': ['Success', 'Failed'],
            'data': [success, failed],
            'chart_type': chart_type
        })
    
    elif chart_type == 'bar':
        # Aggregate by hour for bar chart
        hourly_data = {}
        for log in logs:
            hour_key = log.timestamp.strftime('%H:00')
            if hour_key not in hourly_data:
                hourly_data[hour_key] = []
            if log.response_time:
                hourly_data[hour_key].append(log.response_time)
        
        return jsonify({
            'labels': list(hourly_data.keys()),
            'response_times': [sum(v)/len(v) if v else 0 for v in hourly_data.values()],
            'chart_type': chart_type
        })
    
    else:  # line or area (default)
        return jsonify({
            'labels': [log.timestamp.strftime('%H:%M') for log in logs],
            'response_times': [log.response_time if log.response_time else 0 for log in logs],
            'status_codes': [log.status_code for log in logs],
            'timestamps': [log.timestamp.isoformat() for log in logs],
            'chart_type': chart_type
        })

@main_bp.route('/api/analytics/<int:api_id>')
@login_required
def get_analytics(api_id):
    """Get analytics for an API"""
    api = API.query.get_or_404(api_id)
    if api.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    hours = request.args.get('hours', 24, type=int)
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    
    logs = APILog.query.filter(
        APILog.api_id == api_id,
        APILog.timestamp >= cutoff
    ).all()
    
    if not logs:
        return jsonify({
            'total_requests': 0,
            'success_count': 0,
            'avg_response_time': 0,
            'uptime': 0
        })
    
    success_count = len([l for l in logs if l.status_code == 200])
    avg_response = sum(l.response_time for l in logs if l.response_time) / len([l for l in logs if l.response_time]) if any(l.response_time for l in logs) else 0
    
    return jsonify({
        'total_requests': len(logs),
        'success_count': success_count,
        'failure_count': len(logs) - success_count,
        'avg_response_time': round(avg_response, 2),
        'uptime': round((success_count / len(logs) * 100), 2) if logs else 0,
        'success_rate': round((success_count / len(logs) * 100), 2) if logs else 0
    })
