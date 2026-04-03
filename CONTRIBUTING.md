# 🤝 Contributing to API Monitor

Thank you for your interest in contributing to the API Monitor project! This document provides guidelines and instructions for contributing.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Commit Messages](#commit-messages)

---

## 📜 Code of Conduct

By participating in this project, you agree to:

- **Be Respectful** - Treat all contributors with respect
- **Be Constructive** - Provide helpful feedback and suggestions
- **Be Inclusive** - Welcome people from all backgrounds and experience levels
- **Be Professional** - Keep discussions focused and productive

---

## 🚀 Getting Started

### Fork the Repository

1. Go to: https://github.com/ArshithaR/API-MONITOR-PROJECT
2. Click **"Fork"** button (top right)
3. Clone your fork locally:

```bash
git clone https://github.com/YOUR-USERNAME/API-MONITOR-PROJECT.git
cd api-monitor-project
```

### Add Upstream Remote

```bash
git remote add upstream https://github.com/ArshithaR/API-MONITOR-PROJECT.git
git remote -v  # Verify both origin and upstream
```

---

## 💻 Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov flake8  # Development tools
```

### 3. Verify Setup

```bash
python app.py
# Should see: Running on http://127.0.0.1:5000

# In another terminal
pytest tests/ -v
# Should see all tests pass
```

### 4. Using Docker (Alternative)

```bash
docker-compose up -d
# Services ready at:
# - http://localhost:5000
# - http://localhost:9090
# - http://localhost:3000
```

---

## ✏️ Making Changes

### Create Feature Branch

```bash
# Update local master
git fetch upstream
git checkout master
git merge upstream/master

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch Naming Convention:**
- Features: `feature/add-notifications`
- Fixes: `fix/database-error`
- Docs: `docs/update-readme`
- Tests: `test/add-monitoring-tests`

### Make Your Changes

Edit files as needed:

```
api/routes.py          # Add new routes
app/models.py          # Modify database models
templates/             # Update UI
tests/                 # Add tests
DEPLOYMENT.md          # Update documentation
```

### Keep Commits Clean

```bash
# Show changes
git status
git diff

# Stage changes (choose option 1 or 2)
# Option 1: Stage all
git add .

# Option 2: Stage specific files
git add app/routes.py tests/test_new_feature.py
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test

```bash
pytest tests/test_app.py -v
pytest tests/test_app.py::test_register -v
```

### Check Code Quality

```bash
flake8 app/
flake8 tests/
```

### Run With Coverage

```bash
pytest tests/ --cov=app --cov-report=html
# Opens: htmlcov/index.html in browser
```

### Before Committing

```bash
# 1. Run all tests
pytest tests/ -v

# 2. Check code quality
flake8 app/ tests/

# 3. Verify app still runs
python app.py
# Ctrl+C to stop

# 4. Test with Docker
docker-compose up -d --build
docker-compose ps          # Should show all 3 services
docker-compose down
```

---

## 📝 Commit Messages

Follow conventional commit format:

### Format

```
<type>: <description>

<body>

<footer>
```

### Types

- **feat** - New feature
- **fix** - Bug fix
- **docs** - Documentation changes
- **test** - Test additions/updates
- **refactor** - Code refactoring
- **style** - Code style (formatting)
- **chore** - Build/dependency updates

### Examples

```
# Good
feat: Add API response caching
fix: Resolve database None value crash
docs: Update deployment guide
test: Add monitoring service tests

# Not good
Fixed stuff
Updated code
Changes
```

### How to Write Good Commits

```bash
# Commit with message
git commit -m "feat: Add email notification on API failure"

# Or use interactive
git commit  # Opens editor for detailed message
```

---

## 📤 Submitting Changes

### 1. Update Your Branch

```bash
git fetch upstream
git rebase upstream/master
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to: https://github.com/YOUR-USERNAME/API-MONITOR-PROJECT
2. Click **"Compare & pull request"**
3. Fill in the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Testing
- [ ] Ran pytest successfully
- [ ] Ran flake8 with no issues
- [ ] Tested manually
- [ ] Added new tests

## Screenshots (if applicable)
[Add screenshots]

## Related Issues
Closes #123
```

### 4. Address Feedback

If reviewers request changes:

```bash
# Make requested changes
git add .
git commit -m "Review: Address feedback on PR"
git push origin feature/your-feature-name

# GitHub automatically updates the PR
```

---

## 🔍 Code Review Checklist

Before submitting, verify:

- [ ] Code follows project style (see below)
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Code quality passes: `flake8 app/`
- [ ] No debug code (`print()`, `breakpoint()`)
- [ ] Documentation updated if needed
- [ ] Commit messages are clear
- [ ] Branch is rebased on upstream/master
- [ ] No merge conflicts

---

## 📐 Coding Standards

### Python Style

Follow **PEP 8** guidelines:

```python
# Good
def get_api_by_id(api_id):
    """Retrieve API monitoring record by ID.
    
    Args:
        api_id: The API identifier
        
    Returns:
        API object or None if not found
    """
    return db.session.query(API).filter_by(id=api_id).first()

# Bad
def getapi(id):
    return db.session.query(API).filter_by(id=id).first()
```

### Documentation

- Use docstrings for functions/classes
- Include type hints where possible
- Comment complex logic
- Update README if user-facing

### File Organization

```python
# Imports at top
from flask import Flask, render_template
from app import db

# Constants
API_TIMEOUT = 30
MAX_RETRIES = 3

# Functions/Classes
class APIMonitor:
    """Main monitoring class."""
    
    def check_api(self, url):
        """Check if API is responding."""
        pass

# Main execution
if __name__ == "__main__":
    app.run()
```

### Naming Conventions

```python
CONSTANT_NAME = "value"      # Constants in UPPER_CASE
function_name()              # Functions in snake_case
ClassName                    # Classes in CamelCase
variable_name = "value"      # Variables in snake_case
_private_method()            # Private methods with _prefix
```

---

## 📚 Documentation Updates

### When to Update Docs

- Adding new feature → Update README.md
- Changing deployment → Update DEPLOYMENT.md
- Database schema changes → Update DATABASE.md
- New API endpoints → Update PROJECT_LINKS.md
- Demo changes → Update DEMO.md

### How to Update Docs

1. Use clear, concise language
2. Include examples
3. Add table of contents for long docs
4. Use markdown formatting
5. Include links to related docs

---

## 🐛 Reporting Issues

Not contributing code? Report issues!

### Before Creating Issue

- [ ] Check existing issues (search first)
- [ ] Test with latest code (run `git pull`)
- [ ] Verify it's a real issue

### Creating Issue

Go to: https://github.com/ArshithaR/API-MONITOR-PROJECT/issues/new

**Include:**

```markdown
## Title
[Clear, concise title]

## Description
What's the problem?

## Steps to Reproduce
1. Do this
2. Then this
3. See this happen

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Environment
- OS: Windows 10 / macOS / Linux
- Python: 3.10 / 3.11 / 3.12
- Docker: yes / no

## Code Snippet
[If applicable]

## Screenshots
[If applicable]
```

---

## 💡 Feature Requests

Have an idea? Share it!

### Create Feature Request

Go to: https://github.com/ArshithaR/API-MONITOR-PROJECT/issues/new

**Include:**

```markdown
## Title
[Clear feature name]

## Problem It Solves
Why do we need this?

## Proposed Solution
How should it work?

## Example Use Case
Show me how you'd use it

## Alternatives Considered
Are there other ways to solve this?
```

---

## 📦 Development Tools

### Useful Commands

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run app
python app.py

# Run tests
pytest tests/ -v

# Check code quality
flake8 app/ tests/

# Format code
black app/ tests/  # (if installed)

# Docker
docker-compose up -d
docker-compose ps
docker-compose logs -f
docker-compose down
```

### Recommended Extensions

If using VS Code:

- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **Pytest** (LittleFox)
- **Docker** (Microsoft)
- **GitLens** (Eric Amodio)

---

## 🎯 Priority Areas

Want to contribute but not sure what? These areas need help:

1. **Testing** - Add more test coverage
2. **Documentation** - Improve and expand docs
3. **Performance** - Optimize database queries
4. **UI/UX** - Improve interface design
5. **Monitoring** - Add more metrics
6. **Deployment** - Add Kubernetes support
7. **Localization** - Translate to other languages

---

## ❓ Getting Help

### Questions?

- **GitHub Discussions:** https://github.com/ArshithaR/API-MONITOR-PROJECT/discussions
- **Issues:** https://github.com/ArshithaR/API-MONITOR-PROJECT/issues
- **Documentation:** See README.md and other docs

### Resources

- [GitHub's Contribution Guide](https://guides.github.com/activities/contributing-to-open-source/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 🎉 Recognition

Contributors who submit merged PRs will be:

1. Added to CONTRIBUTORS.md
2. Mentioned in release notes
3. Recognized in README.md

Thank you for making API Monitor better! 🙏
