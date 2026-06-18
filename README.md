# Expense Tracker

## Overview

A multi-user Expense Tracker built with Flask and SQLite.

Users can register, log in, manage expenses, update profiles, and change passwords. Administrators can view users and all expenses through an admin dashboard.

---

## Features

### Authentication

- User Registration
- User Login
- Logout
- Password Hashing
- Session Management

### Expense Management

- Add Expense
- View Expenses
- Update Expense
- Delete Expense
- Filter Expenses
- Category Summary
- Total Expense Summary

### Profile

- View Profile
- Edit Profile
- Change Password

### Admin

- View Users
- View User Expenses
- Delete Users
- Role-based Access Control

---

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja2

---

## Concepts Learned

- Flask Routing
- Jinja Templates
- SQLite CRUD
- SQL JOINs
- Foreign Keys
- Sessions
- Password Hashing
- Decorators
- Blueprints
- Role-Based Authentication

---

## Project Structure

project/
├── app.py
├── database.py
├── handlers.py
├── validate.py
├── decorators.py
├── routes/
│ ├── auth.py
│ ├── expense.py
│ ├── admin.py
│ └── profile.py
├── templates/
└── static/

---

# Screenshots
## SIGNUP
![SIGN UP FORM](screenshots/signup.png)
## SIGNUP INVALID HANDLEING
![USING ALREADY EXISTS EMAIL](screenshots/signup_chechibg_already _exist_email.png)
![RESULT](screenshots/signup_result.png)


## LOGIN
![LOGIN](screenshots/login.png)
![LOGIN SECURE](screenshots/login_security.png)

## DASHBOARD
![DASHBOARD](screenshots/dashboad.png)
![DASHBOARD INVALID INPUT](screenshots/dashboard_security.png)

## VIEW EXPENSES AND OPERATION
![VIEW EXPENSES](screenshots/view_expenses.png)
![EXPENSE FILTERING](screenshots/expense_filtering.png)
![EXPENSE FILTERING](screenshots/expense_filtering_result.png)
![UPDATE EXPENSE](screenshots/update_expense.png)
![UPDATE EXPENSE FORM](screenshots/update_expense_form.png)
![UPDATE EXPENSE RESULT](screenshots/update_result.png)
![DELETE EXPENSE](screenshots/delete_expense.png)
![DELETE EXPENSE](screenshots/delete_expense__.png)
![DELETE EXPENSE RESULT](screenshots/delete_expense_result.png)

# ADMIN
## ADMIN ROUTE
![AMDIN](screenshots/admin_user.png)
## ADMIN SAUMMARY
![AMDIN SUMMARY](screenshots/admin_summary.png)
## ADMIN USER ALL EXPENSES
![AMDIN USER ALL EXPENSES](screenshots/all_expense.png)




---

## How To Run

1. Clone repository
2. Create virtual environment
3. Install Flask

pip install flask werkzeug

4. Run application

python app.py

5. Open browser

http://127.0.0.1:5000