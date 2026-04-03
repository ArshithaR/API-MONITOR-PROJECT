# 📊 API Monitor

A comprehensive **real-time API monitoring application** built with Flask, Docker, and a complete monitoring stack. Track the health, performance, and availability of your APIs with beautiful dashboards, charts, and analytics.

> **GitHub Repository:** https://github.com/ArshithaR/API-MONITOR-PROJECT.git

---

## 📚 **Documentation Hub**

| Document | Purpose | Time |
|----------|---------|------|
| **[⚡ QUICKSTART.md](QUICKSTART.md)** | Get running in 3-5 minutes | 5 min |
| **[🔗 PROJECT_LINKS.md](PROJECT_LINKS.md)** | All URLs and access points | Quick ref |
| **[📊 DEMO.md](DEMO.md)** | Professional demo script | 30 min |
| **[💾 DATABASE.md](DATABASE.md)** | Database schema & access | Reference |
| **[🚀 DEPLOYMENT.md](DEPLOYMENT.md)** | Full deployment workflow | Reference |

---

## ✨ **Key Features**

- 🔐 **User Authentication** - Secure login and registration system
- 📡 **API Monitoring** - Real-time monitoring of API endpoints
- 📊 **Analytics & Charts** - Line, Area, Bar, and Pie charts
- 📈 **Performance Metrics** - Response time, success rate, uptime tracking
- 📥 **CSV Export** - Export monitoring data for analysis
- 🔔 **Alerts** - Get notified when APIs go down
- 🎯 **Beautiful Dashboard** - Intuitive, responsive interface
- 🐳 **Docker & Compose** - Complete containerized stack
- 📉 **Prometheus Metrics** - Industry-standard metrics collection
- 📊 **Grafana Dashboards** - Beautiful visualization of metrics
- 🔄 **CI/CD Pipeline** - Automated testing and deployment on GitHub

## 🚀 **Quick Start**

### 🐳 **Docker (Recommended - 3 minutes)**

```bash
git clone https://github.com/ArshithaR/API-MONITOR-PROJECT.git
cd api-monitor-project
docker-compose up -d
```

Then visit:
- 🌐 **App:** http://localhost:5000
- 📊 **Prometheus:** http://localhost:9090
- 📈 **Grafana:** http://localhost:3000

### 💻 **Local Installation (5 minutes)**

```bash
git clone https://github.com/ArshithaR/API-MONITOR-PROJECT.git
cd api-monitor-project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then visit: http://127.0.0.1:5000

**➡️ For detailed setup, see [QUICKSTART.md](QUICKSTART.md)**

---

## 🏗️ **Complete Technology Stack**

### Backend & Application
- **Python 3.12** - Modern Python runtime
- **Flask 3.0.0** - Web framework
- **SQLAlchemy 2.0.48** - ORM for database
- **Flask-Login** - User authentication

### Database
- **SQLite3** - File-based database for data persistence
- **File Location:** `instance/database.db`
- **Tables:** users, api, api_log

### Docker & Orchestration
- **Docker 29.1.5+** - Container runtime
- **Docker Compose v5.0.1+** - Multi-container orchestration
- **Services:**
  - **api-monitor** (Port 5000) - Flask application
  - **prometheus** (Port 9090) - Metrics collection
  - **grafana** (Port 3000) - Visualizations & dashboards

### Monitoring Stack
- **Prometheus** - Metrics scraping and storage
- **Grafana** - Time-series data visualization
- **API Observable Metrics** - Response time, status codes, error rates

### Frontend
- **HTML5/CSS3** - Responsive design
- **JavaScript** - Interactive charts and features
- **Chart.js** - Beautiful data visualization

### CI/CD
- **GitHub Actions** - Automated testing and deployment
- **Workflow:** Lint → Test → Docker Build → Deploy

---

## 🗂️ **Project Structure**

```
api-monitor-project/
├── README.md                   # This file
├── QUICKSTART.md              # ⚡ Quick start guide (5 min)
├── PROJECT_LINKS.md           # 🔗 All URLs and endpoints
├── DATABASE.md                # 📊 Database schema & access
├── DEPLOYMENT.md              # 🚀 Deployment workflow
├── DEMO.md                    # 📺 30-minute demo script
├── app.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker container config
├── docker-compose.yml         # Multi-service orchestration
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # GitHub Actions CI/CD
├── app/
│   ├── __init__.py           # Flask factory
│   ├── models.py             # Database models
│   ├── routes.py             # API endpoints
│   └── monitor.py            # Background monitoring
├── templates/                # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── login.html
│   └── ...
├── tests/                    # Unit & integration tests
│   ├── test_app.py
│   └── conftest.py
├── monitoring/               # Monitoring configs
│   ├── prometheus/
│   └── grafana/
└── instance/                 # Database & instance data
    └── database.db          # SQLite database
```

## � **API Endpoints**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/register` | GET/POST | User registration |
| `/login` | GET/POST | User login |
| `/logout` | GET | User logout |
| `/dashboard` | GET | Main monitoring dashboard |
| `/analytics` | GET | Analytics and charts |
| `/devops` | GET | System statistics |
| `/api/add` | POST | Add API to monitor |
| `/api/delete/<id>` | POST | Delete API |
| `/export-csv` | GET | Export monitoring data |

**➡️ For complete endpoint documentation, see [PROJECT_LINKS.md](PROJECT_LINKS.md)**

## � **Live Demonstration**

Ready to demo the project to stakeholders? Follow the [DEMO.md](DEMO.md) script for a **complete 30-minute walkthrough:**

✅ **Part 1: GitHub Repository** (3 min)
- Show commits and CI/CD workflows
- Demonstrate code quality

✅ **Part 2: Docker Deployment** (4 min)
- Show containerized services
- Verify all 3 services running

✅ **Part 3: Database Connection** (5 min)
- Access SQLite and show real data
- Query monitoring records

✅ **Part 4: Live Application** (8 min)
- Register and login
- Add APIs to monitor
- View real-time dashboard and analytics

✅ **Part 5: Monitoring Stack** (2 min)
- Show Prometheus metrics
- Display Grafana dashboards

---

## 📊 **Monitoring Features**

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

## 🔄 **Background Monitor Service**

The application includes a background monitoring service that automatically:
- ✅ Runs every 30 seconds
- ✅ Checks all monitored APIs
- ✅ Records response times and status codes
- ✅ Handles timeouts and errors gracefully
- ✅ Stores data in SQLite database
- ✅ Updates charts in real-time

All data is accumulated over time, showing trends and patterns.

---

## 🧪 **Testing**

Run unit tests:
```bash
pytest tests/ -v
```

---

## 🐳 **Docker & Docker Compose**

### Quick Docker Commands

```bash
# Start all services
docker-compose up -d

# View all running services
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# View database
docker exec -it api-monitor-app sqlite3 /app/instance/database.db
```

### What Each Service Does

| Service | Port | Purpose |
|---------|------|---------|
| **api-monitor** | 5000 | Flask application & dashboard |
| **prometheus** | 9090 | Metrics collection & queries |
| **grafana** | 3000 | Dashboard visualization |

**➡️ For complete deployment guide, see [DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 🔄 **GitHub CI/CD Pipeline**

Every time you push to GitHub, automated workflows run:

```
PUSH TO GITHUB
        ↓
LINT CODE (flake8)
        ↓
RUN TESTS (pytest)
        ↓
BUILD DOCKER IMAGE
        ↓
✅ DEPLOYMENT SUCCESS
```

View workflow status at: https://github.com/ArshithaR/API-MONITOR-PROJECT/actions

**Workflow File:** `.github/workflows/ci-cd.yml`

## 📦 **Requirements**

- Python 3.10+
- Flask 3.0.0
- SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Requests 2.31.0
- Docker 20.10+ (for containerized deployment)
- docker-compose v1.29+ (for multi-service orchestration)

For full requirements, see [requirements.txt](requirements.txt)

---

## 💾 **Database**

The application uses **SQLite3** for data persistence:

| Component | Details |
|-----------|---------|
| **Type** | SQLite3 (file-based) |
| **Location** | `instance/database.db` |
| **Connection String** | `sqlite:///instance/database.db` |
| **ORM** | SQLAlchemy 2.0.48 |
| **Persistence** | Docker volumes preserve data across restarts |

**Tables:**
- `users` - User accounts and authentication
- `api` - API endpoints to monitor
- `api_log` - Monitoring records (timestamps, response times, status codes)

**➡️ For complete database schema and queries, see [DATABASE.md](DATABASE.md)**

---

## 🔐 **Security Notes**

- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Run behind a reverse proxy (nginx, Apache)
- Use HTTPS in production
- Enable CSRF protection
- Regularly backup database: `cp instance/database.db backup.db`

---

## 📝 **Environment Variables**

When deploying to production, set these environment variables:

```bash
FLASK_APP=app.py
FLASK_ENV=production          # production or development
FLASK_DEBUG=0                 # Disable debug mode in production
SECRET_KEY=your-secret-key    # Change! Use a secure random string
DATABASE_URL=sqlite:///instance/database.db
```

For Docker, these are defined in `docker-compose.yml`

---

## 🐛 **Troubleshooting**

### Common Issues

| Issue | Solution |
|-------|----------|
| **App won't start** | Check Python 3.10+: `python --version` |
| **Port already in use** | Change port in docker-compose or use different port |
| **Database errors** | Delete `instance/database.db` and restart |
| **Docker build fails** | Clear cache: `docker system prune -a` |
| **Tests failing** | Install test deps: `pip install pytest` |
| **Grafana won't load** | Wait 30s for services to start: `docker-compose logs` |

**➡️ For detailed troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 🚀 **Production Deployment**

### Using Gunicorn (Recommended)

```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### Using Docker

```bash
docker build -t api-monitor:production .
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  --name api-monitor \
  api-monitor:production
```

### Using docker-compose

```bash
docker-compose -f docker-compose.yml up -d --build
```

**➡️ For complete deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 📚 **Documentation Reference**

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | Get running in 3-5 minutes |
| [PROJECT_LINKS.md](PROJECT_LINKS.md) | All URLs and access points |
| [DATABASE.md](DATABASE.md) | Database schema and SQL queries |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment workflow |
| [DEMO.md](DEMO.md) | 30-minute demo script |

---

## 📄 **License**

This project is open source and available under the MIT License.

---

## 👨‍💻 **Author**

Created by **Rakshitha R**

**GitHub:** https://github.com/ArshithaR

---

## 🤝 **Contributing**

Contributions are welcome! Please follow these steps:

1. Fork the repository: https://github.com/ArshithaR/API-MONITOR-PROJECT.git
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📞 **Support & Issues**

Found a bug or have a question?

1. **Check Existing Issues:** https://github.com/ArshithaR/API-MONITOR-PROJECT/issues
2. **Create New Issue:** Click "New Issue" with details
3. **Discussions:** Use GitHub Discussions for questions

---

## ✨ **Acknowledgments**

- Flask for the web framework
- SQLAlchemy for ORM
- Docker for containerization
- Prometheus for metrics
- Grafana for visualization
- Chart.js for charts
- GitHub Actions for CI/CD

---

## 🔗 **Quick Links**

| Link | Purpose |
|------|---------|
| [GitHub Repository](https://github.com/ArshithaR/API-MONITOR-PROJECT) | Main repository |
| [Issues](https://github.com/ArshithaR/API-MONITOR-PROJECT/issues) | Bug reports and features |
| [Releases](https://github.com/ArshithaR/API-MONITOR-PROJECT/releases) | Version history |
| [GitHub Pages](https://arshithar.github.io/API-MONITOR-PROJECT) | Project website |
| [Docker Hub](https://hub.docker.com/r/arshithar/api-monitor) | Docker images |

---

**Last Updated:** January 2025

**Status:** ✅ Production Ready | 🚀 Actively Maintained | 📝 Fully Documented
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section

---

**Made with ❤️ for API monitoring**
