# 📦 Deployment Guide - Complete Workflow

**Perfect deployment workflow with GitHub, Docker, and Database.**

---

## 🎯 Deployment Overview

```
LOCAL DEVELOPMENT
        ↓
GITHUB PUSH
        ↓
CI/CD TESTS
        ↓
DOCKER BUILD
        ↓
PRODUCTION DEPLOYMENT
        ↓
MONITORING ACTIVE
```

---

## 📍 **Step 1: Development Setup**

### Clone Repository

```bash
# Clone from GitHub
git clone https://github.com/ArshithaR/API-MONITOR-PROJECT.git
cd api-monitor-project

# Verify remote
git remote -v
# origin  https://github.com/ArshithaR/API-MONITOR-PROJECT.git (fetch)
# origin  https://github.com/ArshithaR/API-MONITOR-PROJECT.git (push)
```

### Install Dependencies (Local)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Verify installation
python -c "from app import create_app; print('✓ App ready')"
```

### Local Development

```bash
# Run application
python app.py

# Visit: http://localhost:5000
# Logs show:
# * Running on http://127.0.0.1:5000
# * WARNING in development
```

---

## 🔧 **Step 2: Git Workflow**

### Make Changes

```bash
# Edit files
# Example: Fix bug, add feature, etc.

# Check status
git status

# Add changes
git add .
# OR specific files
git add app/routes.py app/models.py
```

### Commit Changes

```bash
# Commit with meaningful message
git commit -m "Fix: Add missing os import in routes.py"
# OR
git commit -m "Feature: Add CSV export functionality"

# View commit
git log --oneline -1
# Output: 79fe6de Fix: Add missing os import in routes.py
```

### Push to GitHub

```bash
# Push to remote
git push origin master
# Output:
# 0757575..79fe6de  master -> master
# 1 file changed, 1 insertion(+)

# Verify on GitHub
# Visit: https://github.com/ArshithaR/API-MONITOR-PROJECT
# See your commit in commit history
```

---

## ✅ **Step 3: GitHub Actions Workflow**

### Automatic CI/CD

When you push, GitHub automatically runs tests:

```yaml
# File: .github/workflows/ci-cd.yml

Steps:
1. Code Checkout
2. Python Setup (3.12)
3. Install Dependencies
4. Lint Check
5. Run Tests
6. Build Docker Image
7. Test Image
8. Success Notification
```

### Check Workflow Status

```bash
# In terminal
git log --all --oneline | head -1
# Shows commit: 79fe6de

# On GitHub
# Visit: https://github.com/ArshithaR/API-MONITOR-PROJECT/actions
# See green ✓ check next to your commit
```

---

## 🐳 **Step 4: Docker Build & Deployment**

### Option A: Build Locally

```bash
# Build image
docker build -t api-monitor:latest .

# Test image
docker run -p 5000:5000 api-monitor:latest
# Visit: http://localhost:5000
```

### Option B: Use Docker Compose (Recommended)

```bash
# Build both image and stack
docker-compose build

# Start all services
docker-compose up -d

# Verify all services
docker-compose ps
# Output:
# NAME                    STATUS
# api-monitor-app         Up (healthy)
# api-monitor-prometheus  Up
# api-monitor-grafana     Up
```

### Verify Deployment

```bash
# Check containers
docker ps

# View logs
docker-compose logs -f app

# Test endpoints
curl http://localhost:5000
curl http://localhost:9090
curl http://localhost:3000
```

---

## 💾 **Step 5: Database Deployment**

### Database Initialization (Automatic)

When app starts, database is created:

```
AppStart → Flask Creates DB → SQLite File Generated
              ↓
        instance/database.db
              ↓
        Tables auto-created:
        - users
        - api
        - api_log
```

### Verify Database

```bash
# Check if database exists
ls -la instance/database.db

# Access database
sqlite3 instance/database.db

# Check tables
sqlite> .tables
# Output: api  api_log  users

# View schema
sqlite> .schema users
# Shows CREATE TABLE definition
```

### Database in Docker

```bash
# Database persisted in Docker volume
docker-compose ps
# See volume mounting: ./instance:/app/instance

# Access from host
cat instance/database.db

# Access from container
docker exec -it api-monitor-app sqlite3 /app/instance/database.db
sqlite> SELECT COUNT(*) FROM users;
```

---

## 🚀 **Step 6: Production Deployment**

### Pre-Deployment Checklist

```bash
# 1. All tests pass
pytest tests/

# 2. No uncommitted changes
git status
# Output: nothing to commit, working tree clean

# 3. Latest code on GitHub
git log --oneline -1
git push origin master

# 4. Docker image builds
docker build -t api-monitor:production .

# 5. Environment configured
cat .env.production  # (if applicable)

# 6. Database backed up
cp instance/database.db instance/database.backup.db

# 7. Documentation updated
# Check: README.md, DATABASE.md, DEPLOYMENT.md
```

### Deploy to Production

#### Option 1: Local Server

```bash
# Stop development instance
docker-compose down

# Restart in production
docker-compose -f docker-compose.yml up -d

# Enable auto-restart
docker update --restart=always api-monitor-app
docker update --restart=always api-monitor-prometheus
docker update --restart=always api-monitor-grafana
```

#### Option 2: Cloud Deployment (Example: AWS)

```bash
# Push image to Docker Hub
docker tag api-monitor:latest yourusername/api-monitor:latest
docker push yourusername/api-monitor:latest

# Deploy to AWS ECS
aws ecs create-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster production --service-name api-monitor \
  --task-definition api-monitor --desired-count 1
```

#### Option 3: Heroku/Railway Deployment

```bash
# For Heroku - Create Procfile
echo "web: gunicorn app:app" > Procfile

# Push to Heroku remote
git push heroku master

# View logs
heroku logs --tail

# Database auto-backed-up
```

---

## 📊 **Step 7: Monitoring & Verification**

### Health Checks

```bash
# 1. Application Health
curl http://localhost:5000/health || echo "App Down"
# Expected: HTTP 200

# 2. Database Health
docker exec api-monitor-app python -c "
from app import db
db.session.execute(db.text('SELECT 1'))
print('✓ Database OK')
"

# 3. Prometheus Scrape
curl http://localhost:9090/api/v1/scrape_pools
# Should show api-monitor as active target

# 4. Container Health
docker inspect api-monitor-app --format="{{.State.Health.Status}}"
# Output: healthy
```

### View Metrics

```bash
# Prometheus metrics
# Visit: http://localhost:9090/graph
# Query: up{job="api-monitor"}
# Result: 1 (healthy) or 0 (down)

# Grafana dashboards
# Visit: http://localhost:3000
# View: API Response Times, Uptime %
```

---

## 🔄 **Step 8: Continuous Updates**

### Regular Maintenance

```bash
# Weekly: Update dependencies
pip list --outdated
pip install --upgrade pip setuptools

# Daily: Check logs
docker-compose logs --tail 100

# Monthly: Database optimization
docker exec api-monitor-app sqlite3 /app/instance/database.db "VACUUM;"

# Quarterly: Full backup
tar -czf backup-$(date +%Y%m%d).tar.gz instance/
```

### Rolling Updates

```bash
# 1. Make code changes locally
# 2. Test thoroughly
# 3. Commit to GitHub
# 4. CI/CD tests run automatically
# 5. Rebuild Docker image
# 6. Deploy new container

# Zero downtime with Docker:
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Traffic redirects automatically
```

---

## 📈 **Complete Deployment Flow Chart**

```
┌─────────────────────────────────────────────────────────────────┐
│                   DEVELOPMENT PHASE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Edit Code → Test Locally → Commit Changes                     │
│       ↓           ↓              ↓                              │
│    app/       python app.py  git commit                         │
│   routes.py   http://5000    git push                           │
│               ✓ Working                                          │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB PHASE                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Repository Updated                                            │
│       ↓                                                          │
│  GitHub Actions Triggered                                      │
│       ↓                                                          │
│  ✓ Tests Pass                                                  │
│  ✓ Lint Pass                                                   │
│  ✓ Docker Build Success                                        │
│       ↓                                                          │
│  Green ✓ on Commit                                             │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DOCKER PHASE                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Docker Image Built                                            │
│       ├─ Python 3.12-slim                                      │
│       ├─ All dependencies                                      │
│       └─ Application code                                      │
│            ↓                                                     │
│  docker-compose up -d                                          │
│       ├─ api-monitor (Flask)                                   │
│       ├─ prometheus (Metrics)                                  │
│       └─ grafana (Dashboards)                                  │
│            ↓                                                     │
│  Volumes Mounted                                               │
│       └─ instance/database.db (Persisted)                      │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DATABASE PHASE                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SQLite Database                                               │
│       ├─ users (Authentication)                                │
│       ├─ api (Endpoints)                                       │
│       └─ api_log (Monitoring Records)                          │
│            ↓                                                     │
│  Data Persistence                                              │
│       ├─ Survives container restart                            │
│       ├─ Backed up daily                                       │
│       └─ Query-able via sqlite3 CLI                            │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              PRODUCTION LIVE PHASE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Application Running                                           │
│       ├─ http://localhost:5000                                 │
│       ├─ http://localhost:9090 (Prometheus)                    │
│       └─ http://localhost:3000 (Grafana)                       │
│            ↓                                                     │
│  Live Monitoring Active                                        │
│       ├─ Users registering                                     │
│       ├─ APIs being monitored                                  │
│       ├─ Real-time data collection                             │
│       └─ Charts updating                                       │
│            ↓                                                     │
│  Health Checks                                                 │
│       ├─ App responding: ✓                                     │
│       ├─ DB connected: ✓                                       │
│       ├─ Prometheus scraping: ✓                                │
│       └─ Grafana visualizing: ✓                                │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
          CONTINUOUS MONITORING & UPDATES
       (Ready for next rollout when needed)
```

---

## ⏱️ Timeline

| Step | Time | Status |
|------|------|--------|
| Setup Dev Environment | 5 min | ✓ |
| Test Locally | 10 min | ✓ |
| Git Push | 1 min | ✓ GitHub |
| CI/CD Tests | 2-3 min | ✓ Automated |
| Docker Build | 3-5 min | ✓ Docker Hub |
| Production Deploy | 2-3 min | ✓ Live |
| **Total** | **~30 min** | **Ready** |

---

## 🆘 Rollback Procedure

If something goes wrong:

```bash
# 1. Stop current deployment
docker-compose down

# 2. Restore previous code
git revert HEAD~1
git push origin master

# 3. Restore previous database (if needed)
cp instance/database.backup.db instance/database.db

# 4. Rebuild and restart
docker-compose up -d --build

# 5. Verify health
curl http://localhost:5000
```

---

## ✅ Post-Deployment

### Verify Everything Works

```bash
# 1. App responds
curl http://localhost:5000

# 2. Database has data
sqlite3 instance/database.db "SELECT COUNT(*) FROM users;"

# 3. Monitoring active
curl http://localhost:9090/-/healthy

# 4. Dashboards loading
curl http://localhost:3000/api/health

# 5. Logs clean
docker-compose logs | grep -i error
```

### Notify Team

```
✅ Deployment Complete!

API Monitor Production Status:
├─ App: https://your-domain.com (or localhost:5000)
├─ Prometheus: http://localhost:9090
├─ Grafana: http://localhost:3000
├─ Database: SQLite active, backed up
└─ Health: All systems operational ✓

Commits Deployed:
- 79fe6de: Add missing os import
- 0757575: Docker quick start

Monitoring: ACTIVE
```

---

**This deployment workflow ensures:**
- ✅ Code quality via CI/CD
- ✅ Automated testing
- ✅ Docker containerization
- ✅ Data persistence
- ✅ Zero downtime updates
- ✅ Full monitoring stack
