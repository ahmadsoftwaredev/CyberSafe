# CyberSafe – Software Testing Report

## 1. Introduction

This document describes the software testing performed on the CyberSafe cybersecurity awareness and protection website.

The purpose of testing was to verify that the implemented features work correctly, user permissions are properly enforced, and the website provides a reliable user experience.

## 2. Testing Objectives

The main objectives of testing were:

- Verify user registration and login functionality.
- Verify role-based access control.
- Test the Password Checker and URL Checker.
- Verify security article management.
- Test quiz creation, attempts, and results.
- Verify quiz history and performance statistics.
- Test administrator dashboard functionality.
- Check website navigation and responsive design.
- Identify and fix any issues discovered during testing.

## 3. Testing Environment

| Component | Environment |
|---|---|
| Operating System | Windows |
| Programming Language | Python 3.14 |
| Backend Framework | Flask 3.1.3 |
| Frontend | HTML, CSS, JavaScript |
| UI Framework | Bootstrap 5 |
| Database | MySQL |
| ORM | Flask-SQLAlchemy |
| Authentication | Flask-Login |
| Browser | Google Chrome |
| Development Environment | Visual Studio Code |

## 4. Testing Approach

Manual functional testing was performed by interacting with the website through the browser.

The testing process included:

- Positive testing: Verifying expected behavior with valid inputs.
- Negative testing: Checking application behavior with invalid inputs.
- Access control testing: Verifying permissions for different user roles.
- UI testing: Checking page layout, navigation, and responsiveness.
- Integration testing: Verifying interactions between related application features.

## 5. Functional Test Cases

### 5.1 Authentication Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| AUTH-01 | Open homepage | Homepage should load successfully | Homepage loaded | Pass |
| AUTH-02 | Register a new user | Account should be created | Registration successful | Pass |
| AUTH-03 | Login as a normal user | Redirect to user dashboard | Redirect successful | Pass |
| AUTH-04 | Login as an administrator | Redirect to admin dashboard | Redirect successful | Pass |
| AUTH-05 | Login with an incorrect password | Login should be rejected | Invalid login rejected | Pass |
| AUTH-06 | Logout from an account | User session should end | Logout successful | Pass |

### 5.2 Role-Based Access Control Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| RBAC-01 | Normal user accesses admin dashboard | Access denied | HTTP 403 returned | Pass |
| RBAC-02 | Normal user accesses admin article management | Access denied | HTTP 403 returned | Pass |
| RBAC-03 | Normal user accesses admin quiz management | Access denied | HTTP 403 returned | Pass |
| RBAC-04 | Administrator accesses admin dashboard | Access allowed | Dashboard opened | Pass |
| RBAC-05 | Logged-out user accesses protected admin pages | Redirect to login | Redirect successful | Pass |
| RBAC-06 | User attempts to access another user's quiz result | Access denied | HTTP 403 returned | Pass |

### 5.3 Security Tips and Article Management Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TIP-01 | Open Security Tips section | Articles should be displayed | Articles displayed | Pass |
| TIP-02 | Open an article | Article details should appear | Details displayed | Pass |
| TIP-03 | Administrator adds an article | Article should be saved | Article added | Pass |
| TIP-04 | Administrator edits an article | Changes should be saved | Changes saved | Pass |
| TIP-05 | Administrator deletes an article | Article should be removed | Article deleted | Pass |
| TIP-06 | Submit an article form with missing required information | Validation should prevent invalid submission | Validation worked | Pass |

### 5.4 Password Checker Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| PWD-01 | Enter a weak password | Weak password assessment should appear | Expected result displayed | Pass |
| PWD-02 | Enter a strong password | Strong password assessment should appear | Expected result displayed | Pass |

### 5.5 URL Checker Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| URL-01 | Submit a valid HTTPS URL | URL assessment should be displayed | Result displayed | Pass |
| URL-02 | Submit an HTTP URL | URL assessment should be displayed | Result displayed | Pass |
| URL-03 | Submit an invalid URL | Invalid input should be handled | Input handled correctly | Pass |

### 5.6 Quiz System Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| QUIZ-01 | Open the Quizzes section | Available quizzes should appear | Quizzes displayed | Pass |
| QUIZ-02 | Start a quiz | Quiz questions should appear | Quiz opened | Pass |
| QUIZ-03 | Submit quiz answers | Answers should be processed | Submission successful | Pass |
| QUIZ-04 | View quiz result | Score and result information should appear | Result displayed | Pass |
| QUIZ-05 | View correct answers | Answer review should be available | Review displayed | Pass |
| QUIZ-06 | Open Quiz History | Previous attempts should appear | History displayed | Pass |
| QUIZ-07 | View performance statistics | Performance information should appear | Statistics displayed | Pass |

### 5.7 Administrator Dashboard Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| ADM-01 | Open Admin Dashboard | Dashboard should load | Dashboard loaded | Pass |
| ADM-02 | View dashboard statistics | Statistics should be displayed | Statistics displayed | Pass |
| ADM-03 | Open Manage Articles | Article management page should open | Page opened | Pass |
| ADM-04 | Open Manage Quizzes | Quiz management page should open | Page opened | Pass |
| ADM-05 | Use Open Dashboard navigation | Appropriate dashboard should open | Navigation worked | Pass |

### 5.8 User Interface and Responsive Testing

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| UI-01 | Check homepage layout | Layout should display correctly | Displayed correctly | Pass |
| UI-02 | Check login and registration pages | Forms should display correctly | Displayed correctly | Pass |
| UI-03 | Check user and admin dashboards | Dashboard elements should be visible | Displayed correctly | Pass |
| UI-04 | Check Security Tips and Tools pages | Content should be properly aligned | Displayed correctly | Pass |
| UI-05 | Check quiz-related pages | Questions and results should display correctly | Displayed correctly | Pass |
| UI-06 | Check navigation and icons | No broken navigation or missing icons | Worked correctly | Pass |
| UI-07 | Check mobile responsive layout | Content should adapt to smaller screens | Layout displayed correctly | Pass |
| UI-08 | Check horizontal scrolling and overlapping elements | No unwanted layout issues | No issues observed | Pass |

## 6. Testing Summary

The manual testing process covered the main functional and interface components of CyberSafe.

| Testing Area | Result |
|---|---|
| Authentication | Passed |
| Role-Based Access Control | Passed |
| Security Article Management | Passed |
| Password Checker | Passed |
| URL Checker | Passed |
| Quiz System | Passed |
| Quiz History and Statistics | Passed |
| Administrator Dashboard | Passed |
| User Interface and Responsiveness | Passed |

All documented test cases passed during the performed manual testing.

## 7. Issues Identified and Resolved

During development and testing, some issues were identified and corrected.

Examples include:

- Correcting quiz result information display.
- Fixing homepage navigation links.
- Verifying role-based dashboard redirection.
- Checking access restrictions for administrator pages.
- Verifying quiz score and answer review functionality.

After applying the corrections, the relevant features were tested again and produced the expected results.

## 8. Known Limitations

- The Password Checker provides a password-strength assessment and does not guarantee that a password is completely secure.
- The URL Checker provides an automated assessment and cannot guarantee that a website is safe.
- Manual testing was performed; this report does not claim automated test-suite execution or formal penetration testing.

## 9. Conclusion

The CyberSafe website successfully passed the documented manual functional and user interface testing scenarios.

The main features, including authentication, role-based access control, security tools, article management, quizzes, quiz history, and administrator functionality, were verified.

The application is considered ready for the next stage of project finalization, subject to deployment configuration and any environment-specific testing.

---

**CyberSafe – Stay Aware. Stay Secure.**