# 🔗 Project Access Links & URLs

## 📍 Main Project Links

### GitHub Repository
- **Repository**: [API-MONITOR-PROJECT](https://github.com/ArshithaR/API-MONITOR-PROJECT.git)
- **Full URL**: `https://github.com/ArshithaR/API-MONITOR-PROJECT.git`
- **How to Access**: 
  1. Open browser
  2. Copy: `https://github.com/ArshithaR/API-MONITOR-PROJECT`
  3. View code, issues, pull requests, workflows

## 🚀 Running Application Links

### Local Development (After `python app.py`)

| Feature | URL | Purpose |
|---------|-----|---------|
| **Home Page** | http://localhost:5000 | Landing page |
| **Register** | http://localhost:5000/register | Create new account |
| **Login** | http://localhost:5000/login | User authentication |
| **Dashboard** | http://localhost:5000/dashboard | View all monitoring data |
| **Analytics** | http://localhost:5000/analytics | View charts & reports |
| **DevOps** | http://localhost:5000/devops | System information |

### Docker Deployment (After `docker-compose up`)

**Same URLs as above:**
- Home: http://localhost:5000
- Dashboard: http://localhost:5000/dashboard
- Analytics: http://localhost:5000/analytics

### Docker Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **Flask App** | http://localhost:5000 | Start here! |
| **Prometheus** | http://localhost:9090 | Metrics collection |
| **Grafana** | http://localhost:3000 | Dashboards (admin/admin) |

## 🎯 Step-by-Step Access Guide

### 1️⃣ **First Time Setup**

```bash
# Clone project
git clone https://github.com/ArshithaR/API-MONITOR-PROJECT.git
cd api-monitor-project

# Visit in browser
# → http://localhost:5000
```

### 2️⃣ **Create Account**

```
Click: http://localhost:5000/register
Fill:
  - Username: testuser
  - Email: test@example.com
  - Password: password123
Click: "Register"
```

### 3️⃣ **Login**

```
Go to: http://localhost:5000/login
Enter: testuser / password123
Click: "Login"
```

### 4️⃣ **Add First API to Monitor**

```
After login, you'll see: http://localhost:5000/dashboard
Click: "Add API" button
Fill:
  - API Name: Google
  - URL: https://www.google.com
  - Check Interval: 300 (seconds)
Click: "Add"
```

### 5️⃣ **View Results**

```
Dashboard: http://localhost:5000/dashboard
  → See real-time status
  → View response times
  → Check uptime percentage

Analytics: http://localhost:5000/analytics
  → View charts
  → Export CSV
  → Date-based reports
```

## 📊 Database Access

### View Database Directly

```bash
# Navigate to project directory
cd api-monitor-project

# Open database
sqlite3 instance/database.db

# Useful queries
sqlite> SELECT * FROM users;
sqlite> SELECT * FROM api;
sqlite> SELECT * FROM api_log ORDER BY timestamp DESC LIMIT 10;
```

### Docker Container Database

```bash
# Access container
docker exec -it api-monitor-app bash

# View database
sqlite3 /app/instance/database.db
sqlite> SELECT COUNT(*) FROM api_log;
```

## 🐳 Docker Compose Services

### Start All Services
```bash
docker-compose up
```

### Access URLs After Starting:

1. **Flask App** → http://localhost:5000
2. **Prometheus** → http://localhost:9090 (Metrics)
3. **Grafana** → http://localhost:3000 (Login: admin/admin)

### View Service Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api-monitor
docker-compose logs -f prometheus
docker-compose logs -f grafana
```

## 🔐 Credentials

### Default Users
| System | Username | Password | Link |
|--------|----------|----------|------|
| **Grafana** | admin | admin | http://localhost:3000 |
| **Test Account** | testuser | password123 | http://localhost:5000/login |

## 📱 Workflow - What to Click

### Complete User Journey:

```
1. START
   ↓
2. Browser → http://localhost:5000
   ↓
3. Click "Register" button
   ↓
4. Fill form → Click "Sign Up"
   ↓
5. Click "Login" button
   ↓
6. Enter credentials → Click "Login"
   ↓
7. You're at Dashboard: http://localhost:5000/dashboard
   ↓
8. Click "+ Add API" button
   ↓
9. Fill API details → Click "Add"
   ↓
10. See API card on dashboard
    ↓
11. Click "Analytics" link
    ↓
12. View charts & data
    ↓
13. Click "Export CSV" to download
```

## 🎬 Live Demo Links

When demonstrating to others, show them:

```
📍 Main App: http://localhost:5000
📊 Dashboard: http://localhost:5000/dashboard  
📈 Analytics: http://localhost:5000/analytics
🐳 Monitoring: http://localhost:9090 (Prometheus)
```

## ✅ Health Check

Open these in sequence to verify everything works:

```bash
1. http://localhost:5000 → App running ✓
2. http://localhost:5000/dashboard → Database connected ✓
3. http://localhost:9090 → Prometheus up ✓
4. http://localhost:3000 → Grafana up ✓
```

## 🔍 API Endpoints (For Developers)

```
GET  /                           Home page
POST /register                   Create account
POST /login                      User login
GET  /dashboard                  Monitoring dashboard
POST /api/add                    Add API to monitor
GET  /api/list                   Get all APIs
GET  /analytics                  Analytics page
GET  /analytics/csv              Export CSV
GET  /devops                     System info
```

---

**Quick Start Command:**
```bash
git clone https://github.com/ArshithaR/API-MONITOR-PROJECT.git
cd api-monitor-project
docker-compose up
# Then visit http://localhost:5000
```
