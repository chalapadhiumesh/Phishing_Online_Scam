# Final Project Demonstration Checklist

This document is a step-by-step guide for presenting the **AI-Based Phishing & Online Scam Intelligence Platform** during your college demonstration or viva.

## 1. Project Startup
1. **Start Database:** Ensure your MySQL server is running (port 3306).
2. **Start Application:** Double-click the `start.bat` file in the project root folder. 
3. **Open Browser:** Navigate to `http://localhost:5173`.

## 2. Walkthrough Sequence

Follow this exact sequence for your demonstration:

1. **Home:** Show the landing page and explain the platform's purpose.
2. **Register:** Create a new test user account (e.g., `examiner@example.com`).
3. **Login:** Log in with the newly created account to demonstrate JWT authentication.
4. **Dashboard:** Show the initial dashboard analytics (scans will be 0).
5. **URL Scan:** Navigate to the URL scanner. Paste a phishing URL (e.g., `http://secure-login-paypal.com-update.info/login`) and scan.
6. **Result (URL):** Show the model's prediction (Phishing) and the high risk score.
7. **History:** Go to the History page to prove the URL scan was immediately saved to the MySQL database.
8. **Message Scan:** Navigate to the Message scanner. Paste a scam message (e.g., `URGENT: Click here to claim your $1000 prize!`) and scan.
9. **Result (Message):** Show the model's prediction (Scam) and the high risk score.
10. **Analytics (Dashboard):** Return to the Dashboard to show the analytics charts and total counts have updated in real-time.
11. **Light/Dark Mode:** Toggle the theme switch in the top navigation bar to demonstrate dynamic CSS variable styling.
12. **Logout:** Click Logout to invalidate the session and return to the Home page.

## 3. Project Architecture (For Viva/Examiner)

**How it works:**
- **Frontend (React + Vite):** A modern, responsive single-page application connecting to the backend via REST APIs.
- **Backend (FastAPI):** A high-performance Python framework handling routing, JWT authentication, and ML orchestration.
- **Machine Learning (Scikit-Learn):** The models (TF-IDF + Logistic Regression) are loaded into memory as a Singleton service when the backend starts, allowing low-latency inference on the unseen text.
- **Database (MySQL + SQLAlchemy):** The ORM maps Python objects to `app_*` tables (e.g., `app_users`, `app_url_scans`), safely managing relational integrity and preventing SQL injection.
