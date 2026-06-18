from flask import session,url_for,redirect
from functools import wraps
def is_logged_in():
    return "user_id" in session

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not is_logged_in():
            return redirect(url_for('auth.user_login'))
        return func(*args,**kwargs)
    return wrapper


def is_admin():
    return session.get("role")=="admin"
def admin_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not is_admin():
            return redirect(url_for('expense.add_expense'))
        return func(*args,**kwargs)
    return wrapper

    
