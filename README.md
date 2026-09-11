# AI-Based Phishing & Online Scam Intelligence Platform

A complete, realistic, production-style academic web application using AI/ML for phishing URL detection and online scam/message detection.

## Local Setup Procedure

Follow these exact steps to run the project on a new computer.

### 1. MySQL Requirement & Database Creation
1. Install and start MySQL Server (e.g., via XAMPP, MySQL Installer, or Workbench).
2. Connect to MySQL as `root` and create the database:
   ```sql
   CREATE DATABASE phishing_scam_platform;
   ```

### 2. Database Schema Execution
The application uses specific `app_*` tables to avoid conflicts.
1. Open your MySQL client or command line.
2. Select the database: `USE phishing_scam_platform;`
3. Execute the provided schema file to create the tables:
   ```bash
   mysql -u root -p phishing_scam_platform < database_schema.sql
   ```

### 3. Environment Configuration (.env)
1. Copy the `.env.example` file and rename it to `.env`.
2. Open `.env` and configure your exact MySQL credentials:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=phishing_scam_platform
   DB_USER=root
   DB_PASSWORD=your_actual_mysql_password
   SECRET_KEY=a_very_long_random_string_for_jwt
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ```

### 4. Python Environment & Dependencies
1. Open a terminal in the root project folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 5. Frontend Dependencies
1. Open a terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```

### 6. Starting the Application
You can start both servers simultaneously by double-clicking the `start.bat` file in the project root. 
Alternatively, start them manually in two terminals:

**Terminal 1 (Backend):**
```bash
.\.venv\Scripts\activate
uvicorn backend.app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### 7. Accessing the Platform
- **Frontend UI:** Open `http://localhost:5173` in your browser.
- **FastAPI Docs (Swagger UI):** Open `http://localhost:8000/docs` to view and interact with the backend API endpoints.

### 8. Running Automated Tests
To run the backend integration tests (requires MySQL and `.env` configured):
```bash
.\.venv\Scripts\activate
pytest tests/test_backend.py -v
```
