#!/usr/bin/env python
import sys
sys.path.insert(0, '.')
from app import create_app
from app.models import db, User, API, Log, HealthScore
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Check for existing data
    user = User.query.first()
    print(f'First user: {user}')
    
    apis = API.query.all()
    print(f'Total APIs: {len(apis)}')
    
    if apis:
        api = apis[0]
        print(f'Using API: {api.id} - {api.name}')
        
        # Check health score
        health = HealthScore.query.filter_by(api_id=api.id).first()
        print(f'Health score: {health}')
        
        if health:
            print(f'  - health_score: {health.health_score}')
            print(f'  - status: {health.status}')
            print(f'  - uptime: {health.uptime_percentage}')
            print(f'  - updated_at: {health.updated_at}')
