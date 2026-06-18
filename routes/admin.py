from flask import Blueprint,url_for,render_template,redirect,request
from decorators import login_required,admin_required
from handlers import handle_user_delete,handle_get_user,handle_user_expense_info,handle_admin_user_with_expenses,handle_admin_get_users
admin_bp=Blueprint("admin",__name__)

@admin_bp.route("/admin/users")
@login_required
@admin_required
def admin_users():
    error=request.args.get("error","").strip()
    if error:
        return render_template("admin_users.html",error=error)
    error,users=handle_admin_get_users()
    if error:
        return render_template("admin_users.html",error=error)
    return render_template("admin_users.html",users=users)

@admin_bp.route("/admin/expenses")
@login_required
@admin_required
def admin_expenses():
    
    error,users=handle_admin_user_with_expenses()
    if error:
        return render_template("admin_expenses.html",error=error)
    
    print(users)
    print(type(users))

    return render_template("admin_expenses.html", users=users)

@admin_bp.route("/admin/summary")
@login_required
@admin_required
def admin_summary():
    
    error,users=handle_user_expense_info()
    if error:
        return render_template("admin_summary",error=error)
    
    return render_template("admin_summary.html",users=users)
    
@admin_bp.route("/admin/user_delete/<int:id>",methods=["POST","GET"])
@login_required
@admin_required
def user_delete_confirmation(id):
    
    error,users=handle_get_user(id)
    users=[users]if users else[]
    if error:
        return redirect(url_for('admin.admin_user',error=error))
    if request.method=="POST":
        error=handle_user_delete(id)
        if error:
            return render_template("admin_user_page.html",error=error)
        return redirect(url_for("admin.admin_users"))
    return render_template("admin_user_page.html",users=users)
