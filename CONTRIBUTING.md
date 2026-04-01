# Contributing to API Monitor 🤝

Thank you for your interest in contributing! We welcome all contributions.

## Getting Started

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/api-monitor.git
cd api-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov pylint black flake8
```

### Running Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_comprehensive.py -v
```

### Code Style

We follow PEP 8 guidelines. Format your code with Black:

```bash
black app/ tests/ --line-length=100
```

Lint your code:
```bash
pylint app/ tests/ --disable=all --enable=E,F
```

## Development Workflow

### 1. Create a Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bugfix branch
git checkout -b bugfix/issue-number
```

Naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes  
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

### 2. Make Changes

- Keep commits atomic and meaningful
- Write clear, descriptive commit messages
- Reference issue numbers when applicable

```bash
# Good commit message
git commit -m "feat: Add real-time monitoring #123"

# Bad commit message
git commit -m "fixed stuff"
```

### 3. Test Your Changes

```bash
# Run tests before pushing
pytest tests/ -v

# Check code quality
black app/ --check
pylint app/
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Detailed description of what was changed and why
- Reference to related issues
- Screenshots (if UI changes)

## Types of Contributions

### Bug Reports

Create an issue with:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/logs if applicable
- Your environment (OS, Python version, etc.)

### Feature Requests

Create an issue with:
- Clear description of the requested feature
- Motivation/use case
- Possible implementation approach
- Relevant examples

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update API documentation
- Add comments for complex logic

### Code Improvements

- Refactor duplicate code
- Improve performance
- Enhance security
- Improve error handling

### Tests

- Add unit tests for new features
- Add integration tests for complex flows
- Improve test coverage
- Add edge case tests

## Code Review Process

Every PR will be reviewed by maintainers. We look for:

1. **Correctness** - Does the code work as intended?
2. **Quality** - Is the code clean and maintainable?
3. **Tests** - Are there sufficient tests?
4. **Documentation** - Is it well documented?
5. **Performance** - Are there performance implications?
6. **Security** - Are there security concerns?

### Responding to Reviews

- Be open to feedback
- Ask questions if something is unclear
- Don't take criticism personally
- Propose alternatives if you disagree

## Commit Message Guidelines

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Type:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style changes
- `refactor` - Code refactoring
- `test` - Test additions
- `chore` - Build/config changes

Example:
```
feat(monitoring): Add real-time health score updates

- Calculate health scores every 5 minutes
- Display score on dashboard
- Alert when score drops below threshold

Fixes #123
```

## Documentation

### Writing Docstrings

```python
def calculate_health_score(api_id):
    """
    Calculate API health score based on uptime and reliability.
    
    Args:
        api_id (int): The ID of the API to calculate score for
        
    Returns:
        tuple: (uptime_percentage, avg_response_time, success_rate, health_score, status)
        
    Raises:
        ValueError: If api_id is invalid
        
    Example:
        >>> uptime, avg_time, success, score, status = calculate_health_score(1)
        >>> score
        95.5
    """
    pass
```

### Updating Documentation

- Update README.md for new features
- Update DEPLOYMENT.md for infrastructure changes
- Add comments for complex algorithms
- Include usage examples

## Testing Guidelines

### Unit Tests

```python
def test_health_score_calculation():
    """Test that health scores are calculated correctly."""
    # Arrange
    api = create_test_api()
    add_test_logs(api.id, success_count=9, failure_count=1)
    
    # Act
    score = calculate_health_score(api.id)
    
    # Assert
    assert score == 95.0  # 9 out of 10 successful
```

### Test Coverage

- Aim for >80% coverage on business logic
- Test edge cases and error conditions
- Test with realistic data

```bash
pytest tests/ --cov=app --cov-report=html --cov-fail-under=80
```

## Performance Considerations

- Profile code before optimizing
- Use indexes for frequently queried columns
- Cache expensive operations
- Avoid N+1 query problems

## Security Best Practices

- Never commit secrets (use .env files and .gitignore)
- Validate and sanitize user input
- Use parameterized queries (SQLAlchemy does this)
- Keep dependencies up to date
- Follow OWASP guidelines

## Release Process

1. Create release branch from main
2. Update version number in appropriate files
3. Update CHANGELOG.md
4. Create GitHub release tag
5. GitHub Actions will build and test automatically

## Getting Help

- Check existing issues and PRs
- Read the documentation
- Ask in PRs/issues
- Check discussions section

## Code of Conduct

- Be respectful and inclusive
- Assume good intentions
- Provide constructive feedback
- Report violations to maintainers

## Recognition

Contributors will be recognized in:
- README.md
- GitHub contributors page
- Release notes

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** We appreciate your effort in making API Monitor better. 🎉
