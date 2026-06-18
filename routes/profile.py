from flask import Blueprint,render_template,redirect,url_for,session,request
from decorators import login_required,admin_required
from handlers import handle_update_password,handle_get_user,handle_edit_profile_username_email

profile_bp=Blueprint("profile",__name__)
@profile_bp.route("/profile")
@login_required
def profile():
    error,user=handle_get_user(session.get("user_id"))
    if error:
        return render_template("profile.html",error=error)
    return render_template("profile.html",user=user)

@profile_bp.route("/edit_profile",methods=["POST","GET"])
@login_required
def edit_profile():
    error,user=handle_get_user(session.get("user_id"))
    if error:
        return render_template("edit_profile.html",error=error)
    if request.method=="POST":
        error=handle_edit_profile_username_email(request.form,session.get("user_id"))
        if error:
            return render_template("edit_profile.html",error=error,user=user)
        return redirect(url_for('profile.profile'))

    return render_template("edit_profile.html",user=user)
    
@profile_bp.route("/update_password",methods=["POST","GET"])
@login_required
def update_password():
    error,user=handle_get_user(session.get("user_id"))
    if error:
        return render_template("update_password.html",error=error)
    if request.method=="POST":
        error=handle_update_password(request.form,session.get("user_id"),user)
        if error:
            return render_template("update_password.html",error=error)
        return redirect(url_for('auth.logout'))
    
    return render_template("update_password.html")
