# 🗄️ Database Configuration Guide

## Database Overview

**API Monitor** uses **SQLite** as the default database - a lightweight, file-based database perfect for monitoring applications.

### Database Connection Details

| Property | Value |
|----------|-------|
| **Database Type** | SQLite3 |
| **Location** | `instance/database.db` |
| **Connection String** | `sqlite:///instance/database.db` |
| **Configuration File** | `app/__init__.py` |
| **ORM Framework** | SQLAlchemy |

## 📊 Database Schema

### Tables

#### 1. **users** - User Authentication
```sql
- id (Primary Key)
- username (String, Unique)
- email (String, Unique)
- password (String, Hashed)
- created_at (DateTime)
```

#### 2. **api** - API Endpoints to Monitor
```sql
- id (Primary Key)
- user_id (Foreign Key → users.id)
- name (String)
- url (String)
- check_interval (Integer, seconds)
- created_at (DateTime)
- is_active (Boolean)
```

#### 3. **api_log** - Monitoring Records
```sql
- id (Primary Key)
- api_id (Foreign Key → api.id)
- status_code (Integer)
- response_time (Float, milliseconds)
- timestamp (DateTime)
- error_message (String, nullable)
```

## 🔌 Connection Configuration

### Local Development (SQLite)
```python
# app/__init__.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

### How to Access Database Directly

```bash
# Open SQLite shell
sqlite3 instance/database.db

# Common queries
sqlite> SELECT * FROM users;
sqlite> SELECT * FROM api WHERE user_id = 1;
sqlite> SELECT * FROM api_log LIMIT 10;
sqlite> .schema  # View all tables
sqlite> .exit
```

## 🐳 Database in Docker

The database file is persisted using Docker volumes:

```yaml
# docker-compose.yml
volumes:
  - ./instance:/app/instance  # Persists database.db
```

### Accessing Docker Database

```bash
# Enter container
docker exec -it api-monitor-app bash

# Access database inside container
sqlite3 /app/instance/database.db
```

## 📈 Database Demonstration

### Step 1: Start the Application
```bash
# Local
python app.py

# OR Docker
docker-compose up
```

### Step 2: Create User Account
- Visit: **http://localhost:5000/register**
- Create account with:
  - Username: `testuser`
  - Email: `test@example.com`
  - Password: `password123`

### Step 3: Add API to Monitor
- Login at **http://localhost:5000/login**
- Click "Add API"
- Fill details:
  - API Name: `Google API`
  - URL: `https://www.google.com`
  - Check Interval: `300` (seconds)

### Step 4: View Database Records

```bash
# Terminal: Check database
sqlite3 instance/database.db

# View all users
SELECT id, username, email FROM users;

# View all APIs being monitored
SELECT id, name, url, user_id FROM api;

# View monitoring logs (last 5)
SELECT * FROM api_log ORDER BY timestamp DESC LIMIT 5;

# Check average response time
SELECT api_id, AVG(response_time) as avg_response FROM api_log GROUP BY api_id;
```

### Step 5: View in Application Interface
- Dashboard: **http://localhost:5000/dashboard**
- Analytics: **http://localhost:5000/analytics**
- API Cards show: Status, Response Time, Uptime %

## 🔄 Data Flow

```
User Registration
       ↓
[users table] ← Store credentials
       ↓
Login → Create Session
       ↓
Add API to Monitor
       ↓
[api table] ← Store endpoint details
       ↓
Background Monitoring (runs every check_interval seconds)
       ↓
[api_log table] ← Store response_time, status_code, timestamp
       ↓
Display in Dashboard/Analytics/Charts
```

## 💾 Backup & Export

### Backup Database
```bash
# Copy database file
cp instance/database.db instance/database.backup.db

# Or from Docker container
docker exec api-monitor-app cp /app/instance/database.db /app/instance/database.backup.db
```

### Export to CSV
- Go to **http://localhost:5000/analytics**
- Click "Export to CSV" button
- Select date range and API

## 🗑️ Database Reset

```bash
# Remove database to start fresh
rm instance/database.db

# Restart application (will create new db)
python app.py
```

## 📝 Model Relationships

```
┌─────────────┐
│    users    │
│  (entities) │
└──────┬──────┘
       │ 1:N
       │
┌──────▼──────┐     1:N      ┌──────────────┐
│     api     │◄─────────────┤  api_log     │
│  (endpoints)│              │  (records)   │
└─────────────┘              └──────────────┘
```

## ✅ Database Health Check

```python
# Check from Python
from app import create_app, db
app = create_app()
with app.app_context():
    # Verify connection
    result = db.session.execute(db.text('SELECT 1'))
    print("✓ Database connection healthy")
    
    # Count records
    users = db.session.query(User).count()
    apis = db.session.query(API).count()
    logs = db.session.query(APILog).count()
    print(f"Users: {users}, APIs: {apis}, Logs: {logs}")
```

---

**For questions about database configuration, refer to `app/models.py` and `app/__init__.py`**
