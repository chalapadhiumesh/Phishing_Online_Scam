# Deployment & Migration Audit Report

## 1. Project Directory Overview
- **frontend/**: React frontend application.
- **backend/**: FastAPI backend application.
- **ml_pipeline/**: Scripts used to train the machine learning models.
- **models/**: Originally contained models, but active models have been moved to `backend/models/`.
- **data/**: Contains raw and processed datasets (CSV files).
- **tests/**: Contains `test_api.py` and `test_e2e.py` for API testing.
- **docs/**: Documentation files.
- **.env** / **.env.example**: Environment variables.
- **.gitignore**: Current version already excludes `.env`, `node_modules`, `__pycache__`, and datasets.

## 2. Frameworks & Package Managers
- **Frontend**: React + Vite (managed via `npm`, `package.json`).
- **Backend**: FastAPI (Python), dependencies managed via `requirements.txt`.
- **Database ORM**: SQLAlchemy (currently using `mysql+pymysql` driver).

## 3. Application Startup
- **Frontend**: Runs via `npm run dev` in the `frontend` folder.
- **Backend**: Runs via `uvicorn backend.app.main:app --port 8000`.
- **Database Setup**: Currently, `Base.metadata.create_all(bind=engine)` is called on startup. There is no active Alembic migration setup (`alembic.ini` is missing).

## 4. Current MySQL Configuration
- The backend connects using the URL format: `mysql+pymysql://<user>:<password>@<host>:<port>/<db_name>`
- Connection parameters are injected from `.env` via `backend/app/core/config.py`.

## 5. Database Tables & Usage
The current MySQL database contains multiple tables. The actively referenced SQLAlchemy models in `backend/app/models/` are:
1. `app_users` (User Model)
2. `app_url_scans` (URLScan Model)
3. `app_message_scans` (MessageScan Model)
4. `app_feedbacks` (Feedback Model)
5. `app_password_resets` (PasswordReset Model)

There are also several legacy tables (`reports`, `scans`, `security_articles`, `phishing_urls`, etc.) discovered via table inspection, likely leftover from Task 3 iterations.

## 6. Environment & Secrets
- Required variables: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`.
- The `.env` file is present locally and correctly added to `.gitignore`. It contains the plaintext DB password and JWT secret.
- No hardcoded secrets were found exposed in the codebase directly.

## 7. Git Status
- A previous attempt to run `git init` by the system failed because the `git` executable is not available in the internal virtual environment's PATH. Git commands must be run via the host terminal or a scripted alternative.
