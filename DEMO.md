# 🎬 Complete Project Demonstration Guide

**How to show:**
1. Perfect running GitHub repository
2. Docker deployment working perfectly  
3. Database connection and data
4. Live application with monitoring

---

## 📋 Pre-Demo Checklist

```bash
# 1. Clone latest from GitHub
git clone https://github.com/ArshithaR/API-MONITOR-PROJECT.git
cd api-monitor-project

# 2. Verify Docker is running
docker --version

# 3. Check git status
git status
git log --oneline -5

# 4. Start the project
docker-compose up -d
```

---

## 🎯 Demo Flow (15-20 minutes)

### **Part 1: GitHub Repository (3 minutes)**

#### Show the Code

```bash
# 1. Open GitHub repository
# → https://github.com/ArshithaR/API-MONITOR-PROJECT

# 2. Show in terminal
git remote -v
# Output should show: origin https://github.com/ArshithaR/API-MONITOR-PROJECT.git

# 3. Show recent commits
git log --oneline -10
# Shows all updates and fixes
```

**What to Point Out:**
- ✅ Active repository with latest updates
- ✅ CI/CD pipeline configured (.github/workflows/ci-cd.yml)
- ✅ Well-structured project organization
- ✅ Docker support with docker-compose.yml
- ✅ Comprehensive documentation

#### Show Repository Content

Click through these sections on GitHub:

| Area | What to Show |
|------|-------------|
| **Code** | `app/` folder structure, models, routes |
| **Commits** | Recent updates and fixes |
| **Actions** | CI/CD workflow status ✓ |
| **Issues** | Project tracking (if any) |
| **Releases** | Version history |

---

### **Part 2: Docker Deployment (4 minutes)**

#### Show Docker Setup

```bash
# 1. Show docker-compose.yml
cat docker-compose.yml
# Shows: api-monitor, prometheus, grafana services

# 2. List running containers
docker ps
# Output:
# CONTAINER ID   IMAGE           NAMES
# abc123...      api-monitor     api-monitor-app
# def456...      prometheus      api-monitor-prometheus
# ghi789...      grafana         api-monitor-grafana
```

#### Show Docker Services Running

```bash
# Check container status
docker-compose ps
# Output shows all 3 services: Up

# View logs
docker-compose logs --tail=50
# Shows successful startup messages
```

**Show in Browser:**

1. **Flask App**: http://localhost:5000 ✓
2. **Prometheus**: http://localhost:9090 ✓
3. **Grafana**: http://localhost:3000 ✓

---

### **Part 3: Database Connection (5 minutes)**

#### Show Database Structure

```bash
# 1. Access the database
sqlite3 instance/database.db

# 2. Show tables
sqlite> .tables
# Output: api  api_log  users

# 3. Show schema
sqlite> .schema
```

#### Show Database Contents

```sql
-- Show all users
sqlite> SELECT id, username, email, created_at FROM users;

-- Show all monitored APIs
sqlite> SELECT id, name, url, user_id FROM api;

-- Show monitoring logs (last 10)
sqlite> SELECT id, api_id, status_code, response_time, timestamp FROM api_log ORDER BY timestamp DESC LIMIT 10;

-- Show statistics
sqlite> SELECT COUNT(*) as total_logs FROM api_log;
```

**Example Output:**

```
Users:
1 | testuser | test@example.com | 2026-04-03 10:00:00

APIs Being Monitored:
1 | Google | https://www.google.com | 1
2 | GitHub | https://www.github.com | 1

Recent Monitoring Logs:
1 | 1 | 200 | 145.32 | 2026-04-03 10:30:15
2 | 1 | 200 | 152.18 | 2026-04-03 10:30:45
```

#### Docker Container Database Access

```bash
# Show database in container
docker exec -it api-monitor-app sqlite3 /app/instance/database.db

# Same queries as above
sqlite> SELECT COUNT(*) FROM api_log;
# Shows data persistence across container restarts
```

---

### **Part 4: Live Application Demo (8 minutes)**

#### Step 1: Show Homepage

**URL**: http://localhost:5000

```
Show:
✓ Beautiful homepage
✓ Login/Register buttons
✓ Project description
✓ Features highlighted
```

#### Step 2: Register New Account

**URL**: http://localhost:5000/register

```
1. Click "Register" button from homepage
2. Fill form:
   - Username: demo_user_[timestamp]
   - Email: demo@example.com
   - Password: DemoPass123!
3. Click "Sign Up"
4. See success message

Result:
✓ New user created in database
✓ Redirected to login page
```

**Verify in Database:**

```bash
sqlite3 instance/database.db
sqlite> SELECT * FROM users WHERE username LIKE 'demo_user%';
```

#### Step 3: Login

**URL**: http://localhost:5000/login

```
1. Enter credentials:
   - Username: demo_user_xyz (or testuser)
   - Password: DemoPass123! (or password123)
2. Click "Login"
3. See secure session established

Show:
✓ Login successful
✓ User authenticated
✓ Session token created
```

#### Step 4: Dashboard

**URL**: http://localhost:5000/dashboard

```
Show:
✓ Real-time API monitoring cards
✓ Current status (✓ Online / ✗ Offline)
✓ Response time in milliseconds
✓ Uptime percentage
✓ Last checked timestamp

Interactions:
1. Click "Add API" button
2. Fill:
   - Name: Google Search
   - URL: https://www.google.com
   - Interval: 300 seconds
3. Click "Add"
4. See new card appear

Verify in Database:
sqlite> SELECT * FROM api WHERE name LIKE 'Google%';
```

#### Step 5: View Monitoring Data

```
After 1-2 minutes of monitoring:

1. Click on API card to see details
2. View endpoint statistics
3. See response time history

Data in Database:
sqlite> SELECT status_code, response_time, timestamp 
        FROM api_log 
        WHERE api_id = (SELECT id FROM api WHERE name = 'Google Search')
        ORDER BY timestamp DESC LIMIT 5;
```

#### Step 6: Analytics Page

**URL**: http://localhost:5000/analytics

```
Show:
✓ Line chart (response time over time)
✓ Area chart (uptime status)
✓ Bar chart (requests per API)
✓ Pie chart (success rate)

Interactive Features:
✓ Hover over data points
✓ Zoom in/out
✓ Legend toggles

Export:
1. Click "Export to CSV"
2. Select date range
3. Download CSV file
4. Show Excel/CSV data

CSV Shows Columns:
- api_name
- timestamp
- response_time
- status_code
- uptime_percentage
```

#### Step 7: DevOps Dashboard

**URL**: http://localhost:5000/devops

```
Show System Information:
✓ Python version
✓ Flask version
✓ Database size
✓ Total monitored APIs
✓ Total monitoring logs
✓ Server uptime

Demonstrates:
✓ Application health
✓ Resource usage
✓ System status
```

---

### **Part 5: Monitoring Stack (2 minutes)**

#### Prometheus Metrics

**URL**: http://localhost:9090

```
Show:
1. Prometheus interface
2. Click "Alerts" tab
3. View metrics being collected
4. Search: http_requests_total
5. View real-time graph
```

#### Grafana Dashboards

**URL**: http://localhost:3000

```
Login: admin / admin

Show:
1. Pre-built dashboards
2. API Response Time dashboard
3. Real-time metrics
4. Data source linked to Prometheus
```

---

## 📊 Complete Workflow Diagram

```
GITHUB REPOSITORY
│
├─ Code (Perfect Structure)
├─ CI/CD Workflow (Automated Tests)
├─ Documentation (README, DATABASE.md)
└─ Latest Commits ✓
         │
         ▼
    GIT CLONE
         │
         ▼
    DOCKER COMPOSE UP
         │
    ┌────┼────┬────────┐
    │    │    │        │
    ▼    ▼    ▼        ▼
  API  PROM GRAFANA  VOLUME
  MON  ESH         (DATABASE)
   │               │
   └────┬──────────┘
        │
        ▼
   SQLITE DATABASE
   ├─ users table
   ├─ api table
   └─ api_log table
        │
        ▼
  APPLICATION LOGIC
  ├─ Register user → users table
  ├─ Add API → api table
  ├─ Monitor → api_log table
  └─ Display → Dashboard/Analytics
        │
        ▼
   BROWSER INTERFACE
   ├─ http://localhost:5000
   ├─ Register & Login
   ├─ Add APIs
   └─ View Results
```

---

## ✅ Demo Checklist

### Before Demo:

- [ ] Git repository cloned
- [ ] Docker running
- [ ] `docker-compose up -d` executed
- [ ] All 3 services started (api-monitor, prometheus, grafana)
- [ ] Test user account exists
- [ ] At least 2 test APIs added
- [ ] 5+ minutes of monitoring data collected
- [ ] Database verified with sqlite3
- [ ] All URLs tested and working

### During Demo:

- [ ] Show GitHub repo and recent commits
- [ ] Demonstrate Docker containers running
- [ ] Show docker-compose.yml structure
- [ ] Access sqlite3 and run queries
- [ ] Create new user account live
- [ ] Add new API while presenting
- [ ] Show real-time monitoring updates
- [ ] Display analytics charts
- [ ] Export CSV file
- [ ] Show DevOps dashboard
- [ ] Access Prometheus and Grafana
- [ ] Query database for created data

### Success Indicators:

✅ GitHub repo accessible and up-to-date
✅ Docker containers running without errors
✅ Application responding on http://localhost:5000
✅ Database connected and data persisting
✅ Real-time monitoring working
✅ Charts updating dynamically
✅ Users can register and login
✅ New APIs can be added
✅ Prometheus scraping metrics
✅ Grafana visualizing data

---

## 🎓 Key Points to Highlight

### 1. **GitHub Workflow**
- "Notice the CI/CD workflow that automatically tests every commit"
- "Database migrations are version controlled"
- "Clear documentation for easy onboarding"

### 2. **Docker Integration**
- "One command deploys entire stack"
- "Three services: Flask, Prometheus, Grafana"
- "Persistent database across container restarts"

### 3. **Database Connection**
- "SQLite for lightweight deployment"
- "Real data from your live monitoring"
- "Easy to verify with simple SQL queries"

### 4. **Live Monitoring**
- "Watch response times update in real-time"
- "Charts update automatically"
- "Data persists permanently in database"

---

## 🚨 Troubleshooting During Demo

| Issue | Solution |
|-------|----------|
| **Port 5000 busy** | `docker-compose down` then up |
| **No monitoring data** | Wait 5 mins for first data collection |
| **Database locked** | Restart containers: `docker-compose restart` |
| **Prometheus not scraping** | Check `monitoring/prometheus/prometheus.yml` |
| **Grafana not loading** | Clear browser cache, try incognito |
| **Docker not running** | Start Docker Desktop application |

---

**Total Demo Time: 20-30 minutes showing:**
- ✅ Perfect GitHub repository (code, commits, CI/CD)
- ✅ Docker deployment (3 services, volumes, networking)
- ✅ Database connection (SQLite, queries, data persistence)
- ✅ Live application (registration, monitoring, analytics)
- ✅ Monitoring stack (Prometheus, Grafana, metrics)
