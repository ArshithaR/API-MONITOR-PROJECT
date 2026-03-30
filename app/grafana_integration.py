"""
Grafana Integration Module
Handles sending metrics to Grafana and managing dashboards
"""
import json
import requests
from datetime import datetime
from app.models import db, API, Log

class GrafanaClient:
    def __init__(self, grafana_url, api_key):
        """Initialize Grafana client"""
        self.grafana_url = grafana_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def create_datasource(self):
        """Create PostgreSQL datasource in Grafana"""
        payload = {
            'name': 'API Monitor Database',
            'type': 'postgres',
            'url': 'db:5432',
            'access': 'proxy',
            'isDefault': True,
            'jsonData': {
                'sslmode': 'disable'
            },
            'secureJsonData': {
                'password': 'secure_password'
            },
            'database': 'api_monitor',
            'user': 'api_monitor'
        }
        
        response = requests.post(
            f'{self.grafana_url}/api/datasources',
            json=payload,
            headers=self.headers
        )
        return response.json() if response.status_code in [200, 201] else None

    def create_dashboard(self):
        """Create API Performance dashboard in Grafana"""
        dashboard = {
            'dashboard': {
                'title': 'API Performance Dashboard',
                'panels': [
                    self._create_panel_uptime(),
                    self._create_panel_latency(),
                    self._create_panel_status_distribution(),
                    self._create_panel_response_times()
                ],
                'schemaVersion': 27,
                'style': 'dark',
                'refresh': '30s'
            },
            'overwrite': True
        }
        
        response = requests.post(
            f'{self.grafana_url}/api/dashboards/db',
            json=dashboard,
            headers=self.headers
        )
        return response.json() if response.status_code in [200, 201] else None

    def _create_panel_uptime(self):
        """Create uptime panel"""
        return {
            'title': 'API Uptime',
            'type': 'stat',
            'targets': [{
                'format': 'table',
                'rawSql': 'SELECT COUNT(*) as uptime FROM log WHERE status_code = 200'
            }],
            'gridPos': {'h': 8, 'w': 12, 'x': 0, 'y': 0}
        }

    def _create_panel_latency(self):
        """Create latency panel"""
        return {
            'title': 'Average Latency (ms)',
            'type': 'graph',
            'targets': [{
                'format': 'time_series',
                'rawSql': 'SELECT timestamp, AVG(response_time) FROM log GROUP BY timestamp'
            }],
            'gridPos': {'h': 8, 'w': 12, 'x': 12, 'y': 0}
        }

    def _create_panel_status_distribution(self):
        """Create status code distribution panel"""
        return {
            'title': 'Status Code Distribution',
            'type': 'piechart',
            'targets': [{
                'format': 'table',
                'rawSql': 'SELECT status_code, COUNT(*) FROM log GROUP BY status_code'
            }],
            'gridPos': {'h': 8, 'w': 12, 'x': 0, 'y': 8}
        }

    def _create_panel_response_times(self):
        """Create response times panel"""
        return {
            'title': 'Response Time Distribution',
            'type': 'histogram',
            'targets': [{
                'format': 'time_series',
                'rawSql': 'SELECT response_time FROM log ORDER BY timestamp DESC LIMIT 1000'
            }],
            'gridPos': {'h': 8, 'w': 12, 'x': 12, 'y': 8}
        }

    def send_metrics(self, api_id, status_code, response_time):
        """Send metrics to Grafana via JSON API"""
        payload = {
            'tags': ['api-monitor'],
            'metrics': [
                {
                    'name': f'api_monitor.response_time',
                    'value': response_time,
                    'timestamp': int(datetime.utcnow().timestamp()),
                    'tags': {'api_id': str(api_id), 'status_code': str(status_code)}
                }
            ]
        }
        
        response = requests.post(
            f'{self.grafana_url}/api/annotations/graphite',
            json=payload,
            headers=self.headers
        )
        return response.status_code in [200, 201]

    def get_dashboard_health(self):
        """Get overall system health"""
        response = requests.get(
            f'{self.grafana_url}/api/health',
            headers=self.headers
        )
        return response.json() if response.status_code == 200 else None

def log_metric_to_grafana(grafana_client, api_id, status_code, response_time):
    """Helper function to log metrics to Grafana"""
    try:
        return grafana_client.send_metrics(api_id, status_code, response_time)
    except Exception as e:
        print(f"Error logging metrics to Grafana: {e}")
        return False
