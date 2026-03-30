import csv
import io
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, Response
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, API, Log
from datetime import datetime

main = Blueprint('main', __name__)

# --- Authentication Routes ---

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('main.register'))
        
        new_user = User(username=username)
        new_user.set_password(password) # Assuming your User model has this method
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password): # Assuming check_password exists
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --- Dashboard & API Routes ---

@main.route('/dashboard')
@login_required
def dashboard():
    apis = API.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', apis=apis)

@main.route('/performance')
@login_required
def performance():
    return render_template('performance.html', title='Performance Analytics')

@main.route('/add_api', methods=['POST'])
@login_required
def add_api():
    name = request.form.get('name')
    url = request.form.get('url')
    interval = request.form.get('interval')
    
    new_api = API(name=name, url=url, interval=interval, user_id=current_user.id)
    db.session.add(new_api)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/delete_api/<int:api_id>')
@login_required
def delete_api(api_id):
    api = API.query.get_or_404(api_id)
    if api.user_id == current_user.id:
        db.session.delete(api)
        db.session.commit()
    return redirect(url_for('main.dashboard'))

# --- Data & Export Routes ---

@main.route('/api/chart_data')
@login_required
def get_chart_data():
    apis = API.query.filter_by(user_id=current_user.id).all()
    return jsonify(build_api_chart_data(apis))

@main.route('/export_csv', methods=['GET', 'POST'])
@login_required
def export_csv():
    if request.method == 'POST':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['API Name', 'URL', 'Status Code', 'Response Time', 'Timestamp'])
        
        apis = API.query.filter_by(user_id=current_user.id).all()
        for api in apis:
            logs = Log.query.filter_by(api_id=api.id).all()
            for log in logs:
                writer.writerow([api.name, api.url, log.status_code, log.response_time, log.timestamp])
        
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=api_logs.csv"}
        )
    return render_template('csv.html')

# --- Helper Functions ---

def build_api_chart_data(apis):
    """Helper used by both the route and your tests"""
    data = {}
    for api in apis:
        # Get latest 10 logs
        logs = Log.query.filter_by(api_id=api.id).order_by(Log.timestamp.desc()).limit(10).all()
        logs.reverse() # Back to chronological order
        
        data[str(api.id)] = {
            'name': api.name,
            'labels': [log.timestamp.strftime('%H:%M:%S') for log in logs],
            'values': [log.response_time for log in logs]
        }
    return data