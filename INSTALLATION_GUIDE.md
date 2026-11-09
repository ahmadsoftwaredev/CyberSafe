# CyberSafe – Installation Guide

This guide explains how to install, configure, and run the CyberSafe application on a local Windows machine.

## 1. System Requirements

Before installation, ensure that the following software is available:

| Software | Requirement |
|---|---|
| Operating System | Windows 10/11 |
| Python | 3.14 |
| MySQL Server | Installed and running |
| MySQL Workbench | Recommended |
| Visual Studio Code | Recommended |
| Git | Recommended |

## 2. Download the Project

Clone the CyberSafe repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project directory:

```bash
cd CyberSafe
```

Alternatively, download and extract the project ZIP file.

## 3. Create a Virtual Environment

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Your terminal should display the virtual environment prefix:

```text
(.venv)
```

## 4. Install Required Packages

Install all project dependencies:

```powershell
pip install -r requirements.txt
```

Wait until the installation process finishes successfully.

## 5. Configure MySQL

Start MySQL Server and open MySQL Workbench.

Create a database:

```sql
CREATE DATABASE cybersafe_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Ensure that your MySQL server is running before proceeding.

## 6. Configure Environment Variables

Create a `.env` file in the root directory of CyberSafe.

Add:

```env
SECRET_KEY=your_secure_secret_key

DATABASE_URL=mysql+pymysql://YOUR_DB_USERNAME:YOUR_DB_PASSWORD@localhost/cybersafe_db
```

Replace the placeholder values with your actual MySQL credentials and a securely generated secret key.

Do not share or upload the `.env` file.

## 7. Initialize Database Tables

Execute:

```powershell
python init_db.py
```

The application will create the database tables using SQLAlchemy.

Expected output:

```text
CyberSafe database tables created successfully!
```

Note: This command creates missing tables; it does not automatically migrate existing database schemas.

## 8. Run CyberSafe

Start the Flask development server:

```powershell
python run.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

The CyberSafe homepage should now appear.

## 9. Access the Application

Available application sections include:

- Home
- About
- User Registration
- User Login
- User Dashboard
- Admin Dashboard
- Security Tips
- Password Checker
- URL Checker
- Cybersecurity Quizzes
- Quiz History

Some sections require authentication, and administrator sections require administrator privileges.

## 10. Troubleshooting

### Database Connection Error

- Ensure MySQL Server is running.
- Verify the database name.
- Check the username and password in `.env`.
- Verify the `DATABASE_URL` format.

### Module Not Found

Activate the virtual environment and run:

```powershell
pip install -r requirements.txt
```

### Port Already in Use

Another application may be using port 5000. Stop that application or configure a different development port.

### Application Secret Key Error

Verify that `SECRET_KEY` is correctly configured in `.env`.

## 11. Important Security Notes

- Never upload `.env` to GitHub.
- Never expose database credentials.
- Do not use Flask debug mode in production.
- Use a production-ready WSGI server when deploying.
- Use strong and unique application secrets.

---

**CyberSafe – Learn, Protect, Stay Secure.**