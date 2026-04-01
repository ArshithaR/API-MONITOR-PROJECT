# 🚀 API Monitor - Professional API Monitoring Dashboard

A comprehensive, production-ready API monitoring solution with real-time analytics, health scoring, alerts, and advanced visualization capabilities.

## Features ✨

### Core Features
- ✅ **Real-Time API Monitoring** - Automatic monitoring of API endpoints with configurable intervals
- ✅ **Performance Analytics** - Detailed response time tracking and analysis
- ✅ **Health Scoring System** - Automated API health calculation based on uptime, speed, and reliability
- ✅ **Alert System** - Intelligent alerts for downtime, slow responses, and recovery events
- ✅ **Dashboard** - Real-time dashboard with status indicators and key metrics
- ✅ **Charts & Visualization** - Multiple chart types (line, bar, pie, area, scatter)
- ✅ **Export Features** - CSV export with advanced filtering options

### Advanced Features
- 📊 **Advanced Analytics** - Success rate, failure rate, uptime percentage, peak usage analysis
- 🚨 **Smart Alerts** - Down/Slow/Recovered alerts with severity levels (critical/warning/info)
- 🧠 **Downtime Prediction** - ML-based prediction of potential downtime
- 📈 **Multi-API Comparison** - Compare performance of multiple APIs side-by-side
- 🎯 **Health Badges** - Visual status indicators (🟢 Excellent, 🟡 Good, 🔴 Poor)
- 📍 **Geo Monitoring** - (Extensible) Regional monitoring support
- ⏱️ **Real-Time Refresh** - Auto-updating dashboards without manual refresh
- 📤 **Export Options** - CSV export with detailed analytics

### API Response Breakdown
- DNS time tracking
- Connection time measurement
- Total response time analysis
- Status code distribution

## Installation 🛠️

### Prerequisites
- Python 3.10+
- SQLite3 (included with Python)
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/api-monitor-project.git
cd api-monitor-project
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

The application will start at `http://127.0.0.1:5000`

## Usage 📖

### First Time Setup
1. Navigate to `http://127.0.0.1:5000` 
2. Click "Register" and create a new account
3. Log in with your credentials

### Adding APIs to Monitor
1. Go to Dashboard
2. Fill in the "Add New API" form:
   - **API Name**: Display name for your API
   - **URL**: Full URL of the API endpoint
   - **Check Interval**: How often to check (in seconds, default: 300)
   - **Latency Threshold**: When to trigger "slow" alert (in ms, default: 1000)
3. Click "Add API"

### Dashboard
- **Real-time Status**: See all your APIs' current status at a glance
- **Health Score**: View each API's health score (0-100)
- **Last Checked**: Timestamp of most recent check
- **Response Time**: Latest response time

### Performance Analytics
- Select an API from the dropdown
- Choose chart type (Line, Bar, Pie, Area, Scatter)
- Select data range (Last 10/20/50/100 records)
- View detailed response time trends

### Alerts
- View all alerts for your APIs
- See severity levels (Critical 🔴, Warning 🟡, Info ℹ️)
- Automatic alerts for:
  - API Down (multiple failed requests)
  - API Too Slow (above threshold)
  - API Recovery (returns online)

### Export Data
- Go to Dashboard and click "Export CSV"
- Download complete API monitoring data
- Includes: API name, URL, status code, response time, timestamp

## Testing 🧪

### Run Unit Tests
```bash
pytest tests/ -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=app --cov-report=html
pytest tests/ --cov=app --cov-report=term-missing
```

### Run Specific Test File
```bash
pytest tests/test_comprehensive.py -v
```

### Run Selenium UI Tests
```bash
pytest tests/test_selenium_ui.py -v
```

## Docker Support 🐳

### Build Docker Image
```bash
docker build -t api-monitor .
```

### Run with Docker
```bash
docker run -p 5000:5000 api-monitor
```

### Docker Compose
```bash
docker-compose up
```

## Project Structure 📁

```
api-monitor-project/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app initialization
│   ├── models.py                # Database models (User, API, Log, etc.)
│   ├── routes.py                # Flask routes and endpoints
│   ├── monitor.py               # Background monitoring task
│   ├── analytics.py             # Analytics calculations
│   └── alerts.py                # Alert management
├── templates/                    # HTML templates
│   ├── layout.html              # Base layout
│   ├── dashboard.html           # Dashboard page
│   ├── performance.html         # Analytics page
│   ├── alerts.html              # Alerts page
│   ├── compare.html             # API comparison
│   ├── login.html               # Login page
│   └── register.html            # Registration page
├── tests/                        # Test files
│   ├── conftest.py              # Pytest configuration
│   ├── test_comprehensive.py    # Unit tests
│   └── test_selenium_ui.py      # UI tests
├── app.py                        # Main application entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
└── README.md                     # This file
```

## Database Models 🗄️

### User
- id (Primary Key)
- username (Unique)
- email
- password_hash
- apis (Relationship to API)
- alerts (Relationship to Alert)

### API
- id (Primary Key)
- name
- url
- user_id (Foreign Key)
- interval (check interval in seconds)
- threshold_latency (alert threshold)
- is_down (boolean status)
- logs (Relationship to Log)
- health_scores (Relationship to HealthScore)

### Log
- id (Primary Key)
- api_id (Foreign Key)
- status_code
- response_time
- dns_time
- connection_time
- timestamp

### HealthScore
- id (Primary Key)
- api_id (Foreign Key)
- uptime_percentage
- avg_response_time
- success_rate
- health_score (0-100)
- status (excellent/good/poor)
- updated_at

### Alert
- id (Primary Key)
- api_id (Foreign Key)
- user_id (Foreign Key)
- alert_type (down/slow/recovered)
- message
- severity (critical/warning/info)
- created_at
- is_read
- is_resolved

## API Endpoints 🔌

### Authentication
- `GET /` - Home page
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - Main dashboard
- `POST /add_api` - Add new API
- `POST /delete_api/<id>` - Delete API

### Analytics
- `GET /performance` - Performance analytics page
- `GET /api/analytics/<api_id>` - Get analytics data (JSON)
- `GET /api/chart-data/<api_id>` - Get chart data (JSON)
- `GET /api/health/<api_id>` - Get health score (JSON)
- `GET /api/prediction/<api_id>` - Get downtime prediction (JSON)

### Alerts
- `GET /alerts` - View all alerts
- `GET /api/alerts/unread` - Get unread alerts count (JSON)
- `POST /alert/<id>/read` - Mark alert as read

### Export
- `GET /export/csv` - Export to CSV
- `GET /export/pdf` - Export to PDF (planned)

### Comparison
- `GET /compare` - Compare APIs page
- `POST /api/compare` - Compare data (JSON)

## API Response Examples 📊

### GET /api/analytics/1
```json
{
  "api_name": "My API",
  "total_requests": 150,
  "success_count": 145,
  "failure_count": 5,
  "success_rate": 96.67,
  "avg_response_time": 145.23,
  "min_response_time": 89.50,
  "max_response_time": 2345.89
}
```

### GET /api/health/1
```json
{
  "health_score": 95.5,
  "status": "excellent",
  "status_badge": "🟢 Excellent",
  "uptime": 99.5,
  "avg_response_time": 150.23,
  "success_rate": 98.0,
  "updated_at": "2024-01-15T10:30:45.123456"
}
```

## Configuration ⚙️

### Environment Variables
Create a `.env` file in the root directory:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database.db
```

### Monitoring Interval
Default monitoring interval is 300 seconds (5 minutes). Configure per API in dashboard.

### Alert Threshold
Default latency threshold is 1000ms. Configure per API in settings.

## Troubleshooting 🐛

### Application won't start
- Ensure Python 3.10+ is installed: `python --version`
- Check all dependencies: `pip install -r requirements.txt`
- Delete old database: `rm instance/database.db`

### No data showing on dashboard
- Ensure APIs have been added
- Wait for background monitor to run (checks every 10 seconds)
- Check API URLs are accessible

### Tests failing
- Run `pytest tests/ -v` for detailed output
- Ensure test database is clean: `rm test.db`
- Install test dependencies: `pip install pytest pytest-cov selenium`

## Contributing 🤝

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

For issues and questions:
- Open an Issue on GitHub
- Check existing documentation
- Review test files for usage examples

## Roadmap 🗺️

- [ ] Multi-user team support
- [ ] Slack/Email notifications
- [ ] Advanced prediction models
- [ ] API response header analysis
- [ ] Custom metrics tracking
- [ ] Performance benchmarking
- [ ] API versioning support
- [ ] Webhook integrations

## Technologies Used 🛠️

- **Backend**: Flask 3.0, SQLAlchemy, Flask-Login
- **Database**: SQLite
- **Frontend**: Bootstrap 5, Chart.js
- **Testing**: Pytest, Selenium
- **DevOps**: Docker, Docker Compose, GitHub Actions
- **Monitoring**: APScheduler

## Authors 👨‍💻

- Rakshitha R - Initial development

## Acknowledgments 🙏

- Flask community for excellent documentation
- Bootstrap for responsive UI components
- Chart.js for beautiful data visualization
- All contributors and testers

---

**Star this project if you find it useful!** ⭐
