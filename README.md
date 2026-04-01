# 📊 API Monitor

A comprehensive API monitoring application built with Flask that tracks the health, performance, and availability of your APIs in real-time.

## ✨ Features

- 🔐 **User Authentication** - Secure login and registration
- 📡 **API Monitoring** - Real-time monitoring of API endpoints
- 📊 **Analytics & Charts** - Multiple chart types (Line, Area, Bar, Pie)
- 📈 **Performance Metrics** - Response time, success rate, uptime tracking
- 📥 **CSV Export** - Export monitoring data for analysis
- 🔔 **Alerts** - Get notified when APIs go down
- 🎯 **Dashboard** - Beautiful, intuitive interface
- 🐳 **Docker Support** - Easy deployment with Docker Compose

## 🚀 Quick Start

### Option 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/ArshithaR/API-MONITOR-PROJECT.git
cd api-monitor-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit **http://127.0.0.1:5000** in your browser.

### Option 2: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t api-monitor .
docker run -p 5000:5000 api-monitor

# For background mode
docker-compose up -d
```

Visit **http://localhost:5000** in your browser.

## 📋 Default Credentials

The app initializes with a fresh database. Create your account on first login:
- **Username:** Choose a username
- **Email:** Enter your email
- **Password:** Create a secure password

## 🗂️ Project Structure

```
api-monitor-project/
├── app.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .github/
│   └── workflows/        # GitHub Actions CI/CD
├── app/
│   ├── __init__.py      # Flask app factory
│   ├── models.py        # Database models
│   ├── routes.py        # API endpoints & views
│   ├── monitor.py       # Background monitoring task
│   └── __pycache__/
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── dashboard.html   # Dashboard view
│   ├── analytics.html   # Analytics & charts
│   ├── csv_data.html    # CSV data viewer
│   └── ...
├── tests/               # Unit tests
│   ├── test_app.py      # Application tests
│   └── __init__.py
└── instance/            # Database file (auto-created)
```

## 🛠️ API Endpoints

### Authentication
- `GET/POST /auth/login` - User login
- `GET/POST /auth/register` - User registration
- `GET /auth/logout` - User logout

### Dashboard
- `GET /dashboard` - Main dashboard
- `GET /analytics` - Analytics page with charts
- `GET /csv` - CSV data viewer
- `POST /api/add` - Add new API to monitor
- `POST /api/delete/<id>` - Delete monitored API

### Data
- `GET /api/chart-data/<id>` - Chart data JSON
- `GET /api/analytics/<id>` - Analytics metrics
- `GET /export-csv` - Download CSV file

## 📊 Monitoring Features

### Chart Types
- **Line Chart** - Smooth response time trends
- **Area Chart** - Filled response time visualization
- **Bar Chart** - Hourly average response times
- **Pie Chart** - Request status distribution

### Metrics Tracked
- ✅ Success Rate (%)
- 📈 Average Response Time (ms)
- 📡 Uptime (%)
- 🔢 Total Requests
- ❌ Failed Requests

## 🔄 Background Monitor

The application includes a background monitoring service that:
- Runs every 30 seconds
- Checks all monitored APIs
- Records response times and status codes
- Handles timeouts and connection errors gracefully

## 🧪 Testing

Run unit tests:
```bash
pytest tests/ -v
```

## 🐳 Docker Commands

```bash
# Build image
docker build -t api-monitor .

# Run container
docker run -p 5000:5000 api-monitor

# Using Docker Compose
docker-compose up
docker-compose up -d          # Background
docker-compose down           # Stop services
docker-compose logs -f        # View logs

# Remove old images
docker system prune
```

## 📦 Requirements

- Python 3.10+
- Flask 3.0.0
- SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Requests 2.31.0

For full requirements, see [requirements.txt](requirements.txt)

## 🔐 Security Notes

- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Run behind a reverse proxy (nginx, Apache)
- Use HTTPS in production
- Enable CSRF protection

## 📝 Environment Variables

```bash
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database.db
```

## 🐛 Troubleshooting

### App won't start
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Docker build fails
```bash
# Clear Docker cache
docker system prune -a

# Rebuild
docker build --no-cache -t api-monitor .
```

### Database issues
```bash
# Remove old database
rm instance/database.db

# Restart application - database will be recreated
```

## 🚀 Deployment

### Production Server
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up Nginx or Apache as reverse proxy
3. Enable SSL/TLS certificates
4. Use environment variables for secrets
5. Set up log rotation

### Docker Deployment
```bash
docker pull api-monitor:latest
docker run -d -p 5000:5000 --name api-monitor api-monitor:latest
```

## 📚 Documentation

- [Architecture](ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)
- [Deployment Guide](DEPLOYMENT.md)

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by Rakshitha R

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

---

**Made with ❤️ for API monitoring**
