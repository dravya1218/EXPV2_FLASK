from flask import Blueprint,render_template,url_for,redirect,session,request
from handlers import handle_registration,handle_login

auth_bp=Blueprint("auth",__name__)
@auth_bp.route("/login",methods=["GET","POST"])
def user_login():
    if request.method=="POST":
        
        error,user=handle_login(request.form)
        if error:
            return render_template("login.html",error=error)
        session["user_id"]=user["id"]
        session["user_username"]=user["username"]
        session["role"]=user["role"]
        if session.get("role")=="admin":
            return redirect(url_for('admin.admin_users'))

        return redirect(url_for("expense.add_expense"))

    return render_template("login.html")

@auth_bp.route("/sign_up",methods=["GET","POST"])
def user_sign_up():
    if request.method=="POST":
        error=handle_registration(request.form)
        if error:
            return render_template("sign_up.html",error=error)
        return redirect(url_for('auth.user_login'))
        
    return render_template("sign_up.html")

@auth_bp.route("/logout")
def logout():
    session.clear()

    return redirect(url_for('auth.user_login'))
