# ⚡ Quick Start Guide

**Get the API Monitor running in 5 minutes.**

---

## 🚀 **Option 1: Docker (Recommended - 3 minutes)**

### Step 1: Clone & Enter Directory

```bash
git clone https://github.com/ArshithaR/API-MONITOR-PROJECT.git
cd api-monitor-project
```

### Step 2: Start Everything

```bash
docker-compose up -d
```

**That's it!** All 3 services start automatically:
- ✅ API Monitor: http://localhost:5000
- ✅ Prometheus: http://localhost:9090
- ✅ Grafana: http://localhost:3000

### Step 3: Verify Running

```bash
docker-compose ps
```

You should see:
```
NAME                    STATUS          PORTS
api-monitor-app         Up (healthy)    0.0.0.0:5000->5000/tcp
api-monitor-prometheus  Up              0.0.0.0:9090->9090/tcp
api-monitor-grafana     Up              0.0.0.0:3000->3000/tcp
```

---

## 💻 **Option 2: Local Python (5 minutes)**

### Step 1: Clone Repository

```bash
git clone https://github.com/ArshithaR/API-MONITOR-PROJECT.git
cd api-monitor-project
```

### Step 2: Create & Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Application

```bash
python app.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
```

---

## 🎯 **First Steps**

### 1. Register Account

Open: **http://localhost:5000/register**

```
Username: testuser
Email: test@example.com
Password: password123
Confirm: password123
```

Click **Register**

### 2. Login

Open: **http://localhost:5000/login**

```
Username: testuser
Password: password123
```

Click **Login**

### 3. Add API to Monitor

On dashboard, click **"Add New API"**

```
API Name: jsonplaceholder
URL: https://jsonplaceholder.typicode.com/posts/1
Check Interval: 60 (seconds)
```

Click **Add API**

### 4. View Dashboard

You'll see:
- ✅ API Name
- 📊 Status
- ⏱️ Response Time
- 📈 Charts

### 5. Check Analytics

Click **"Analytics"** tab to see:
- 📊 Response time graphs
- 📈 Uptime percentage
- 🔴 Error rates

### 6. Export Data

On Dashboard, click **"Export CSV"** to download monitoring data

---

## 🔗 **Important URLs**

| Service | URL | Purpose |
|---------|-----|---------|
| **API Monitor** | http://localhost:5000 | Main application |
| **Prometheus** | http://localhost:9090 | Metrics (advanced) |
| **Grafana** | http://localhost:3000 | Dashboards (admin/admin) |

---

## 🐳 **Docker Commands**

### View Logs

```bash
docker-compose logs -f app
```

### Stop Services

```bash
docker-compose down
```

### Restart Services

```bash
docker-compose restart
```

### Access Database

```bash
docker exec -it api-monitor-app sqlite3 /app/instance/database.db
.tables
SELECT COUNT(*) FROM users;
.quit
```

---

## 📂 **Project Structure**

```
api-monitor-project/
├── app/
│   ├── routes.py      # API endpoints
│   ├── models.py      # Database models
│   └── monitor.py     # Monitoring logic
├── templates/         # HTML pages
├── instance/          # Database (created after first run)
├── Dockerfile         # Container config
├── docker-compose.yml # Multi-service
└── requirements.txt   # Dependencies
```

---

## ✅ **Verification Checklist**

- [ ] Docker version 20.10+ installed (`docker --version`)
- [ ] docker-compose working (`docker-compose version`)
- [ ] Port 5000 available (no other app using it)
- [ ] Port 9090 available
- [ ] Port 3000 available
- [ ] http://localhost:5000 loads
- [ ] Account registration works
- [ ] Can add APIs to monitor
- [ ] Dashboard shows data

---

## 🆘 **Troubleshooting**

### "Connection refused" on localhost:5000

```bash
# Check if container is running
docker-compose ps

# If not running, start it
docker-compose up -d

# Check logs
docker-compose logs app
```

### "Port already in use"

```bash
# Find what's using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                  # macOS/Linux

# Or use different port
PORT=8000 docker-compose up -d
# Then access http://localhost:8000
```

### "Database not found"

This is normal on first run. The database is created automatically.

```bash
# Verify database was created
docker exec api-monitor-app ls -la /app/instance/database.db
```

### Tests Failing

```bash
# Run tests locally
python -m pytest tests/

# If pytest not installed
pip install pytest
python -m pytest tests/
```

---

## 📚 **Full Documentation**

For more details, see:
- **[DATABASE.md](DATABASE.md)** - Database schema and data
- **[PROJECT_LINKS.md](PROJECT_LINKS.md)** - All URLs and endpoints
- **[DEMO.md](DEMO.md)** - How to demonstrate the project
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment

---

## 🎓 **Common Tasks**

### Add Multiple APIs

1. Dashboard → "Add New API"
2. Enter details (GitHub API, weather API, etc.)
3. Repeat
4. Monitor all in one dashboard

### Export Data

1. Dashboard → "Export CSV"
2. Open in Excel/Google Sheets
3. Analyze response times and uptime

### View System Stats

1. Click "DevOps" menu
2. See CPU, Memory, API stats
3. Identify performance issues

### Change Monitoring Interval

1. Dashboard → Edit API
2. Change "Check Interval"
3. Click "Update"
4. Monitoring frequency changes

---

## 🚨 **Monitoring Your APIs**

The app monitors your APIs by:

1. **Sending HTTP requests** at the interval you set
2. **Recording response time** (how fast it responds)
3. **Capturing status code** (200 = OK, 500 = Error)
4. **Logging errors** (timeout, connection refused, etc.)
5. **Creating charts** showing trends over time

---

## 🎯 **Next Steps**

1. ✅ **Start the app** (Docker or Python)
2. ✅ **Register an account**
3. ✅ **Add an API to monitor**
4. ✅ **Wait 2-3 minutes** to see data
5. ✅ **View dashboard** to see monitoring results
6. ✅ **Check analytics** for charts
7. ✅ **Share with others** - GitHub URL at top of this file

---

## 💡 **Tips**

- **Test APIs**: Use https://jsonplaceholder.typicode.com/ for practice
- **Check Logs**: `docker-compose logs -f` to see real-time activity
- **Share Project**: Use GitHub link: https://github.com/ArshithaR/API-MONITOR-PROJECT.git
- **Backup Data**: `cp instance/database.db backup.db`
- **Monitor from Docker**: All services isolated and scalable

---

**🎉 You're ready to monitor APIs!**
