# 🚀 Quick Start Guide - Docker & GitHub

## Start Application in Docker (3 Easy Steps)

### Step 1: Build Docker Image
```powershell
cd c:\Users\Rakshitha R\OneDrive\Desktop\api-monitor-project
docker-compose build
```

### Step 2: Start Containers
```powershell
docker-compose up -d
```

### Step 3: Access Application
Open browser and go to:
```
http://localhost:5000
```

## 🐳 Docker Commands

### View Running Containers
```powershell
docker ps
```

### View Container Logs
```powershell
docker logs api-monitor-app -f
```

### Stop Application
```powershell
docker-compose down
```

### Rebuild and Restart
```powershell
docker-compose down
docker-compose build
docker-compose up -d
```

## 🐙 GitHub Commands

### Check Status
```powershell
cd c:\Users\Rakshitha R\OneDrive\Desktop\api-monitor-project
git status
```

### Push Changes
```powershell
git add -A
git commit -m "Your message"
git push origin master
```

### View Recent Commits
```powershell
git log --oneline -10
```

### Check Remote
```powershell
git remote -v
```

## ✨ Key Features in Docker

- ✅ **Persistent Database**: SQLite data saved in `instance/` volume
- ✅ **Background Monitor**: API checking every 30 seconds
- ✅ **Health Checks**: Container status verified every 30s
- ✅ **Auto Restart**: Container restarts on failure
- ✅ **Port 5000**: Application accessible via http://localhost:5000

## 📊 Application URL

**Local (Python)**: http://127.0.0.1:5000  
**Docker**: http://localhost:5000

Both work the same way!

## 🔗 GitHub Repository

https://github.com/ArshithaR/API-MONITOR-PROJECT.git

Your project is now visible and synchronized with GitHub!

---

**Status**: ✅ Docker Running | ✅ GitHub Connected | ✅ Ready for Production
