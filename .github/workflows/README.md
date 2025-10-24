# GitHub Actions Workflows

This directory contains automated workflows for the OSINT Story Aggregator project.

## Available Workflows

### 🧪 Tests (`test.yml`)
**Triggers:** Push to main/master/claude/* branches, Pull requests

Tests the application across multiple Python versions:
- Python 3.8, 3.9, 3.10, 3.11
- Runs basic functionality tests
- Verifies all imports work correctly
- Caches pip dependencies for faster runs

**Status Badge:**
```markdown
![Tests](https://github.com/arandomguyhere/News_Feeder/actions/workflows/test.yml/badge.svg)
```

### 🎨 Lint (`lint.yml`)
**Triggers:** Push to main/master/claude/* branches, Pull requests

Code quality checks:
- flake8: Syntax errors and code quality
- black: Code formatting standards

**Status Badge:**
```markdown
![Lint](https://github.com/arandomguyhere/News_Feeder/actions/workflows/lint.yml/badge.svg)
```

### 🔒 Security (`security.yml`)
**Triggers:** Push to main/master, Pull requests, Weekly schedule (Sundays)

Security scanning:
- Safety: Checks dependencies for known vulnerabilities
- Bandit: Scans code for security issues
- Uploads security reports as artifacts

**Status Badge:**
```markdown
![Security](https://github.com/arandomguyhere/News_Feeder/actions/workflows/security.yml/badge.svg)
```

## Adding to README

Add these badges to your main README.md:

```markdown
![Tests](https://github.com/arandomguyhere/News_Feeder/actions/workflows/test.yml/badge.svg)
![Lint](https://github.com/arandomguyhere/News_Feeder/actions/workflows/lint.yml/badge.svg)
![Security](https://github.com/arandomguyhere/News_Feeder/actions/workflows/security.yml/badge.svg)
```

## Running Locally

You can run the same checks locally before pushing:

```bash
# Install test dependencies
pip install flake8 black safety bandit pylint

# Run tests
python test_aggregator.py

# Run linting
flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
black --check src/

# Run security scan
safety check
bandit -r src/
```

## Future Workflows

Potential additions:
- **Deploy**: Automated deployment to cloud services
- **Release**: Automated versioning and release creation
- **Coverage**: Code coverage reporting
- **Documentation**: Auto-generate and deploy docs
- **Scheduled Run**: Run the aggregator on schedule and commit reports
