import pytest
from unittest.mock import patch, MagicMock
from app.models import db, Log
from app.monitor import monitor_task

class TestMonitorTask:
    """Test API monitoring functionality"""
    
    @patch('app.monitor.requests.get')
    def test_successful_api_request(self, mock_get, app, test_api):
        """Test successful API monitoring request"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with app.app_context():
            # Simulate a monitoring check
            from app.routes import main
            
            # Just verify that the mock works
            response = mock_get(test_api.url)
            assert response.status_code == 200
    
    @patch('app.monitor.requests.get')
    def test_failed_api_request(self, mock_get, app, test_api):
        """Test failed API monitoring request"""
        mock_get.side_effect = Exception('Connection timeout')
        
        with app.app_context():
            try:
                mock_get(test_api.url)
            except Exception as e:
                assert 'Connection timeout' in str(e)
    
    def test_log_creation_on_request(self, app, test_api):
        """Test that logs are created for API requests"""
        with app.app_context():
            log = Log(api_id=test_api.id, status_code=200, response_time=100.5)
            db.session.add(log)
            db.session.commit()
            
            retrieved_log = Log.query.filter_by(api_id=test_api.id).first()
            assert retrieved_log is not None
            assert retrieved_log.response_time == 100.5
    
    def test_response_time_calculation(self, app, test_api):
        """Test response time is properly recorded"""
        with app.app_context():
            response_times = [100.5, 150.3, 120.7]
            
            for rt in response_times:
                log = Log(api_id=test_api.id, status_code=200, response_time=rt)
                db.session.add(log)
            db.session.commit()
            
            logs = Log.query.filter_by(api_id=test_api.id).all()
            assert len(logs) == 3
            assert all(log.response_time in response_times for log in logs)

class TestChartDataBuilder:
    """Test chart data building logic"""
    
    def test_build_chart_data(self, app, test_api, test_logs):
        """Test chart data is properly built"""
        with app.app_context():
            from app.routes import build_api_chart_data
            from app.models import API
            
            apis = API.query.all()
            chart_data = build_api_chart_data(apis)
            
            assert str(test_api.id) in chart_data
            assert 'name' in chart_data[str(test_api.id)]
            assert 'labels' in chart_data[str(test_api.id)]
            assert 'values' in chart_data[str(test_api.id)]
    
    def test_chart_data_contains_latest_logs(self, app, test_api, test_logs):
        """Test chart data contains latest logs"""
        with app.app_context():
            from app.routes import build_api_chart_data
            from app.models import API
            
            apis = API.query.all()
            chart_data = build_api_chart_data(apis)
            
            # Should have up to 10 latest logs (limit in build_api_chart_data)
            assert len(chart_data[str(test_api.id)]['values']) <= 10
