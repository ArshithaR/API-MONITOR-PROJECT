# API Performance Monitor - Project Structure

## Directory Structure

```
api-monitor-project/
├── app/
│   ├── __init__.py
│   ├── models.py              # Database models
│   ├── routes.py              # Flask routes
│   ├── monitor.py             # Background monitoring task
│   ├── grafana_integration.py # Grafana integration
│   └── __pycache__/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── test_models.py         # Database model tests
│   ├── test_routes.py         # Route/API tests
│   ├── test_monitor.py        # Monitor logic tests
│   └── test_selenium.py       # UI tests
│
├── templates/
│   ├── layout.html            # Base template
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main dashboard
│   ├── performance.html       # Performance analytics
│   ├── charts.html            # Chart page
│   ├── csv.html               # CSV export page
│   ├── manage.html            # API management
│   └── devops.html            # DevOps dashboard
│
├── docker/
│   └── [Docker-related files]
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions workflow
│
├── app.py                     # Flask app factory
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Multi-container setup
├── prometheus.yml             # Prometheus configuration
├── analysis.ipynb             # Jupyter analysis notebook
│
├── DEPLOYMENT.md              # Deployment guide
├── ARCHITECTURE.md            # System architecture
└── README.md                  # Project README
```

## File Descriptions

### Core Application Files

**app.py**
- Flask app factory
- Database initialization
- Login manager setup
- Background monitoring startup

**app/models.py**
- User model (authentication)
- API model (monitored endpoints)
- Log model (performance data)

**app/routes.py**
- Authentication routes (login, register, logout)
- Dashboard routes
- API management routes (add, delete)
- Data export routes
- Chart data endpoints

**app/monitor.py**
- Background monitoring task
- API health checks
- Response time measurement
- Log recording

**app/grafana_integration.py**
- Grafana client for API communication
- Dashboard creation
- Metric sending
- Data source management

### Testing Files

**tests/conftest.py**
- Pytest fixtures
- Test database setup
- Mock user creation
- Test API setup

**tests/test_models.py**
- Database model validation
- Relationship testing
- Cascade delete testing

**tests/test_routes.py**
- Route functionality testing
- Authentication testing
- API management testing
- Export functionality testing

**tests/test_monitor.py**
- API monitoring logic
- Response recording
- Chart data building

**tests/test_selenium.py**
- Browser automation
- UI interaction testing
- Form submission
- Navigation testing

### Template Files

**templates/layout.html**
- Base template
- Navigation bar
- Styling and scripts

**templates/dashboard.html**
- Main dashboard
- Add new API form
- Monitored endpoints table

**templates/performance.html**
- Performance analytics
- Multiple chart types
- Graph type selectors

**templates/login.html & register.html**
- Authentication UI

### Configuration Files

**Dockerfile**
- Python 3.11 slim base
- Dependency installation
- Port exposure
- Health checks

**docker-compose.yml**
- Web service (Flask app)
- Database service (PostgreSQL)
- Grafana service
- Prometheus service
- Network configuration

**.github/workflows/ci-cd.yml**
- GitHub Actions workflow
- Test job
- Build job
- Deploy job
- Notify job

**requirements.txt**
- Flask and extensions
- Testing frameworks
- Monitoring tools
- Database drivers

### Documentation Files

**DEPLOYMENT.md**
- Detailed deployment instructions
- Testing procedures
- Docker commands
- CI/CD setup
- Grafana configuration
- Troubleshooting guide

**ARCHITECTURE.md**
- System architecture diagram
- Component relationships
- Data flow
- Technology stack

**README.md**
- Project overview
- Quick start guide
- Feature list
- Contributing guidelines

## Key Features by Layer

### Authentication Layer
- User registration
- Password hashing
- Session management
- Login protection

### Monitoring Layer
- Background API checks
- Response time measurement
- Status code recording
- Error tracking

### Data Layer
- SQLAlchemy ORM
- PostgreSQL database
- Log aggregation
- Data persistence

### Visualization Layer
- Dashboard UI
- Multiple chart types
- Real-time updates
- CSV export

### Monitoring & Alerting
- Grafana dashboards
- Threshold alerts
- Multi-channel notifications
- Historical analysis

### Testing Layer
- Unit tests (pytest)
- UI tests (Selenium)
- Coverage reporting
- Security scanning

### Deployment Layer
- Docker containerization
- Docker Compose orchestration
- GitHub Actions CI/CD
- Auto-deployment

## Dependencies

### Runtime
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Requests 2.31.0
- APScheduler 3.10.4
- Gunicorn 21.2.0
- psycopg2-binary 2.9.9

### Testing
- pytest 7.4.3
- pytest-cov 4.1.0
- Selenium 4.15.2

### Analysis
- Jupyter 1.0.0
- pandas (via Jupyter)
- matplotlib (via Jupyter)

### Monitoring
- grafana-api 1.0.3
- python-dotenv 1.0.0

## Configuration Management

Environment variables (via .env or docker-compose):
- `FLASK_ENV` - development/production
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask session key
- `GRAFANA_URL` - Grafana API endpoint
- `GRAFANA_API_KEY` - Grafana authentication

## Database Schema

**users table**
- id (PK)
- username (UNIQUE)
- password

**apis table**
- id (PK)
- user_id (FK)
- name
- url
- interval

**logs table**
- id (PK)
- api_id (FK)
- status_code
- response_time
- timestamp

## API Endpoints

- `GET /` - Redirect to dashboard
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout
- `GET /dashboard` - Main dashboard (protected)
- `GET /performance` - Performance analytics (protected)
- `POST /add_api` - Add new API (protected)
- `GET /delete_api/<id>` - Delete API (protected)
- `GET /api/chart_data` - Get chart data (protected, JSON)
- `GET /export_csv` - CSV export form (protected)
- `POST /export_csv` - Download CSV (protected)

## Deployment Workflow

1. **Development**
   - Write code and tests locally
   - Run pytest locally
   - Test with Flask dev server

2. **Version Control**
   - Commit to GitHub
   - Push to feature branch
   - Create pull request

3. **CI Pipeline**
   - GitHub Actions triggered
   - Tests run automatically
   - Code coverage checked
   - Security scan performed

4. **Build**
   - Docker image built
   - Pushed to registry
   - Tagged with version and latest

5. **Deploy**
   - Pull image to production
   - Run docker-compose
   - Health checks performed
   - Notifications sent

6. **Monitor**
   - Grafana dashboards active
   - Alerts configured
   - Logs aggregated
   - Metrics collected

---

**Last Updated**: March 2024
**Version**: 1.0.0
