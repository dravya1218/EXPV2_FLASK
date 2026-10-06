import os
from flask import Flask,render_template,redirect,url_for,request,session
from functools import wraps
from handlers import *
from database import *
from decorators import login_required,admin_required
from routes.auth import auth_bp
from routes.expense import expense_bp
from routes.admin import admin_bp
from routes.profile import profile_bp

create_user_table()
create_expense_table()
app=Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_fallback_key_only")
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(admin_bp)



if __name__=="__main__":
    app.run(debug=True)