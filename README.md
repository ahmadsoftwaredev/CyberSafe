# CyberSafe – Cybersecurity Awareness & Protection Website

CyberSafe is a web-based cybersecurity awareness platform developed using Python and Flask. It helps users improve their cybersecurity knowledge, evaluate password strength, identify suspicious URLs, read security articles, and test their knowledge through interactive quizzes.

The platform provides separate access for normal users and administrators, with role-based access control and an administration dashboard.

## Key Features

### 1. User Authentication
- User registration and login.
- Secure password hashing.
- Session management using Flask-Login.
- Role-based access for normal users and administrators.
- Separate dashboard redirection for users and administrators.

### 2. Password Checker
- Evaluates password strength.
- Checks password length and character combinations.
- Provides feedback to help users create stronger passwords.
- Performs password analysis in the browser.

### 3. URL Checker
- Analyzes URLs for common suspicious indicators.
- Identifies potentially risky URL characteristics.
- Provides warnings based on URL analysis.
- Does not visit or fetch the submitted URL.

*Note: The URL Checker provides basic indicator-based analysis, not a guaranteed security verdict.*

### 4. Security Tips & Articles
- Browse cybersecurity awareness articles.
- View individual article details.
- Administrators can add, edit, and delete security articles.

### 5. Interactive Cybersecurity Quizzes
- Browse available quizzes.
- Attempt multiple-choice questions.
- Automatically calculate quiz scores.
- View quiz results and correct answers.
- Review selected answers and explanations.
- Administrators can manage quizzes and questions.

### 6. Quiz History & Performance Tracking
- View previous quiz attempts.
- Track total attempts.
- View best and average scores.
- Monitor quiz-wise performance.
- Access previous quiz results.

### 7. Admin Dashboard
- View total registered users.
- View total security articles.
- View total quizzes and questions.
- View total quiz attempts.
- Access article and quiz management sections.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.14 |
| Backend Framework | Flask 3.1.3 |
| Frontend | HTML5, CSS3, JavaScript |
| UI Framework | Bootstrap 5 |
| Database | MySQL |
| ORM | Flask-SQLAlchemy |
| Database Driver | PyMySQL |
| Authentication | Flask-Login |
| Form Security | Flask-WTF |
| Database Migrations | Flask-Migrate |
| Environment Configuration | python-dotenv |
| Version Control | Git |

## Project Structure

```text
CyberSafe/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── quiz.py
│   │   ├── tips.py
│   │   └── tools.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   │
│   │   └── js/
│   │       ├── password_checker.js
│   │       └── url_checker.js
│   │
│   └── templates/
│       ├── admin/
│       ├── admin_dashboard.html
│       ├── dashboard.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── password_checker.html
│       ├── url_checker.html
│       ├── tips.html
│       ├── tip_detail.html
│       ├── quizzes.html
│       ├── quiz_attempt.html
│       ├── quiz_result.html
│       └── quiz_history.html
│
├── config.py
├── init_db.py
├── requirements.txt
├── run.py
├── .gitignore
└── .env
```

## Installation & Setup

Follow these steps to run CyberSafe on your local machine.

### Prerequisites

Make sure you have installed:

- Python 3.14
- MySQL Server
- MySQL Workbench (recommended)
- Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd CyberSafe
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database

1. Start your MySQL Server.
2. Open MySQL Workbench.
3. Create a database named `cybersafe_db`.
4. Use the `utf8mb4` character set.

Example SQL:

```sql
CREATE DATABASE cybersafe_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 5. Configure Environment Variables

Create a `.env` file in the project's root directory.

Add the following configuration:

```env
SECRET_KEY=replace_with_a_secure_random_secret_key

DATABASE_URL=mysql+pymysql://YOUR_DB_USERNAME:YOUR_DB_PASSWORD@localhost/cybersafe_db
```

Replace the database username and password with your own MySQL credentials.

**Important:**
- Never upload your `.env` file to GitHub.
- Use a strong, randomly generated secret key.
- If your database password contains special characters, URL-encode them in the database connection URL.

### 6. Initialize Database Tables

Run:

```powershell
python init_db.py
```

This script creates the database tables using Flask-SQLAlchemy.

Expected output:

```text
CyberSafe database tables created successfully!
```

### 7. Run the Application

Start the Flask development server:

```powershell
python run.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

CyberSafe should now be running locally.

## Security Considerations

CyberSafe incorporates several security practices:

- Passwords are stored as hashes rather than plain text.
- Login-protected routes require authentication.
- Administrator routes enforce role-based authorization.
- CSRF protection is initialized through Flask-WTF.
- SQLAlchemy ORM is used for database operations.
- Environment variables are used for sensitive configuration.
- The URL Checker analyzes submitted text without fetching external URLs.

**Production note:** The current `run.py` configuration uses Flask debug mode for local development. Debug mode must be disabled in production. A production deployment should also use a secure secret key and a production-ready WSGI server.

## Project Purpose

The purpose of CyberSafe is to promote cybersecurity awareness by providing accessible educational resources and simple interactive tools. It demonstrates the development of a full-stack web application with authentication, database integration, administrative functionality, and interactive learning features.

## License

This project was developed as an educational software development project. No open-source license has been specified.
