from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file, make_response
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, API, Log
import csv as csv_lib  # Aliased to prevent AttributeError: 'function' object has no attribute 'writer'
import io
import requests
import time

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('main.register'))
        new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

def build_api_chart_data(apis):
    chart_data = {}
    for api in apis:
        logs = Log.query.filter_by(api_id=api.id).order_by(Log.timestamp.desc()).limit(10).all()
        logs.reverse() 
        chart_data[str(api.id)] = {
            'name': api.name,
            'labels': [log.timestamp.strftime('%H:%M:%S') for log in logs],
            'values': [log.response_time for log in logs]
        }
    return chart_data

@main.route('/dashboard')
@login_required
def dashboard():
    apis = API.query.filter_by(user_id=current_user.id).all()
    api_status = {}
    for api in apis:
        latest_log = Log.query.filter_by(api_id=api.id).order_by(Log.timestamp.desc()).first()
        if latest_log:
            api_status[api.id] = {
                'status': 'Active' if latest_log.status_code == 200 else 'Inactive',
                'response_time': latest_log.response_time,
                'speed': 'Fast' if latest_log.response_time < 500 else 'Slow'
            }
        else:
            api_status[api.id] = {'status': 'No data', 'response_time': 0, 'speed': 'Unknown'}
    api_chart_data_json = build_api_chart_data(apis)
    return render_template('dashboard.html', apis=apis, api_status=api_status, api_chart_data=api_chart_data_json)

@main.route('/api/chart_data')
@login_required
def get_api_chart_data(): 
    apis = API.query.filter_by(user_id=current_user.id).all()
    return jsonify(build_api_chart_data(apis))

@main.route('/performance')
@login_required
def performance():
    apis = API.query.filter_by(user_id=current_user.id).all()
    api_chart_data_json = build_api_chart_data(apis)
    return render_template('performance.html', apis=apis, api_chart_data=api_chart_data_json)

@main.route('/add_api', methods=['POST'])
@login_required
def add_api():
    name = request.form.get('name')
    url = request.form.get('url')
    interval = int(request.form.get('interval', 60))
    new_api = API(name=name, url=url, interval=interval, user_id=current_user.id)
    db.session.add(new_api)
    db.session.commit()
    try:
        start = time.time()
        r = requests.get(url, timeout=5)
        latency = (time.time() - start) * 1000
        log = Log(api_id=new_api.id, status_code=r.status_code, response_time=round(latency, 2))
    except:
        log = Log(api_id=new_api.id, status_code=0, response_time=0)
    db.session.add(log)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/delete_api/<int:id>')
@login_required
def delete_api(id):
    api = API.query.get_or_404(id)
    if api.user_id == current_user.id:
        db.session.delete(api)
        db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/export_csv', methods=['GET', 'POST']) 
@login_required
def export_csv():
    if request.method == 'POST':
        output = io.StringIO()
        writer = csv_lib.writer(output) 
        writer.writerow(['API Name', 'URL', 'Timestamp', 'Status Code', 'Response Time (ms)'])
        logs = Log.query.join(API).filter(API.user_id == current_user.id).order_by(Log.timestamp.desc()).all()
        for log in logs:
            writer.writerow([log.api.name, log.api.url, log.timestamp, log.status_code, log.response_time])
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='api_performance_report.csv'
        )
    return render_template('csv.html')