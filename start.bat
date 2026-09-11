@echo off
echo "Starting AI-Based Phishing & Online Scam Intelligence Platform..."

echo Starting Backend Server (FastAPI)...
start cmd /k ".\.venv\Scripts\uvicorn backend.app.main:app --reload --port 8000"

echo Starting Frontend Server (React+Vite)...
start cmd /k "cd frontend && npm run dev"

echo Both servers are starting.
echo Backend API Docs: http://localhost:8000/docs
echo Frontend App: http://localhost:5173
pause
