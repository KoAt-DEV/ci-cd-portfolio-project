# Python CI/CD Portfolio: FastAPI + SQLAlchemy Web App

![CI](https://github.com/KoAt-DEV/ci-cd-portfolio-project/actions/workflows/ci.yml/badge.svg?branch=main) 
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This repository showcases a modern Python web application built with FastAPI and SQLAlchemy 2.0+ (async support), complete with a robust GitHub Actions CI pipeline. The pipeline enforces linting, type checking, and comprehensive testing across multiple Python versions, ensuring high code quality and reliability. It's designed as a portfolio project to demonstrate best practices in Python development, CI/CD, and database integration.

The app includes user authentication (JWT-based), CRUD operations, and async database interactions with PostgreSQL. All tests run against a real PostgreSQL container, with Alembic for migrations.

## Features

### Backend Framework
- FastAPI with async endpoints for high-performance APIs
- Database: SQLAlchemy 2.0+ (declarative mapping with Mapped types) and asyncpg for async queries; psycopg for sync migrations
- Authentication: JWT tokens (HS256 algorithm) with secure password hashing
- Migrations: Alembic for database schema management

### CI/CD Pipeline
- **Linting & Style**: Black (formatter), Ruff (linter), Flake8 (style checker), Bandit (security scanner)
- **Type Checking**: MyPy with full SQLAlchemy 2.0 support (no plugins needed)
- **Testing**: Pytest with 85%+ coverage; matrix testing on Python 3.10, 3.11, and 3.12; PostgreSQL service container for integration tests
- **Artifacts**: HTML coverage reports uploaded per Python version
- **Security**: Secrets management via GitHub Secrets (e.g., DB_URL, SECRET_KEY)
- **Performance**: Pip caching for faster CI runs

## Quick Start (Local Development)

### Prerequisites
- Python 3.10+ (recommend 3.12 for full feature parity)
- PostgreSQL (local or Docker)
- Git

### Setup

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/KoAt-DEV/ci-cd-portfolio-project.git
   cd ci-cd-portfolio
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   Copy .env.example to .env and fill in your values:
   ```
   DB_URL=postgresql+asyncpg://user:pass@localhost:5432/yourdb
   TEST_DB_URL=postgresql+asyncpg://testuser:testpass@localhost:5432/testdb
   SYNC_TEST_DB_URL=postgresql+psycopg://testuser:testpass@localhost:5432/testdb
   ALGORITHM=HS256
   SECRET_KEY=your-super-secret-key-here  # Generate a strong one!
   ```

5. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Run the App**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

Visit http://localhost:8000/docs for interactive API docs (Swagger UI).

### Development Tasks

**Run Tests**:
```bash
pytest --cov=app --cov-report=html
```
Open `htmlcov/index.html` in your browser for coverage details.

**Type Check & Lint**:
```bash
mypy app --config pyproject.toml
black --check app
ruff check app
flake8 app
bandit -r app
```

## CI/CD Pipeline Overview

The pipeline triggers on pushes to main or manual dispatch. It consists of three parallel jobs:
1. **Lint & Style**: Enforces code formatting and security
2. **Typecheck**: Validates types with MyPy (SQLAlchemy 2.0+ compatible)
3. **Functional Tests**: Matrix across Python versions with PostgreSQL container; includes migrations and coverage reporting

View live runs in the Actions tab. All jobs must pass for a successful build.

### Example Workflow Highlights
- **Matrix Testing**: Ensures compatibility across Python 3.10–3.12
- **Database Service**: Uses Dockerized PostgreSQL with health checks for reliable integration tests
- **Coverage Artifacts**: Downloadable HTML reports per version for detailed analysis

## Project Structure

```
ci-cd-portfolio/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entrypoint
│   ├── models/              # SQLAlchemy models (e.g., base.py, usermodel.py)
│   ├── crud/                # CRUD operations (e.g., usercrud.py)
│   ├── routers/             # API routes (e.g., userauth.py)
│   ├── services/            # Business logic (e.g., auth.py)
│   └── db.py                # Database session management
├── tests/                   # Pytest integration/unit tests
├── alembic/                 # Migration scripts
├── .github/workflows/       # CI YAML files
├── requirements.txt         # Dependencies
├── pyproject.toml          # MyPy/Flake8 config
└── README.md
```

## Why This Project?

This portfolio demonstrates practical skills in:
- Building scalable async APIs with FastAPI and SQLAlchemy
- Implementing robust CI/CD with GitHub Actions (linting, typing, testing)
- Handling real-world concerns like migrations, security, and multi-version support

It started as a simple app and evolved through iterative debugging (e.g., resolving MyPy issues with SQLAlchemy 2.0 declarative mapping)—a testament to problem-solving in production-like environments.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by FastAPI and SQLAlchemy documentation
- Thanks to the open-source community for tools like Ruff, MyPy, and Pytest

Built with ❤️ for Python enthusiasts. Questions? Open an issue or reach out on LinkedIn!
