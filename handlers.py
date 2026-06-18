from database import *
from form_validate import *
from werkzeug.security import generate_password_hash,check_password_hash
def handle_registration(form):
    error,username,email,password=user_sign_up_form(form)
    if error:
        return error
    
    user_username=get_user_username(username)
    if user_username:
        return "username already exists"
    
    user_email=get_users_email(email)
    if user_email:
        return "email already exists"
    hash_password=generate_password_hash(password)
    success=insert_user(username,email,hash_password)
    if not success:
        return "username email already exists"
    return None

def handle_login(form):
    error,email,password=user_login_form(form)
    if error:
        return error,None
    user=get_users_email(email)
    if not user:
        return"no user found of this email",None
    
    user_hash_password=user["password_hash"]
    valid_password=check_password_hash(user_hash_password,password)
    if not valid_password:
        return "invalid password",None
    return None,user

def handle_add_update_expense(mode,form,user_id,id=None,):
    error,name,amount,category=add_expense_form(form)
    if error:
        return error
    if mode=="add":
        success=insert_expense(name,amount,category,user_id)
        if not success:
            return "cannot add expense"
    if mode=="update":
        success=update(user_id,id,name,amount,category)
    return None

def handle_filtering(user_id,name,category,min_amount,max_amount):
    expenses=filtering(user_id,name,category,min_amount,max_amount)
    if not expenses:
        return "No expenses found",None
    return None,expenses

def handle_total_summary(user_id,name,category,min_amount,max_amount):
    result=total_expense_summary(user_id,name,category,min_amount,max_amount)
    result=dict(result)
    if result["count"]==0:
        result["total"]=0
        result["count"]=0
        return result
    return result
def handle_category_summary(user_id,name,category,min_amount,max_amount):
    category_summary=total_category_summary(user_id,name,category,min_amount,max_amount)
    if not category_summary:
        return []
    return category_summary

def handle_get_expense(user_id,id):
    expense=get_expense(user_id,id)
    if not expense:
        return"No expense found",None
    return None,expense

def handle_delete(user_id,id):
    success=delete_expense(user_id,id)
    if not success:
        return "No expense found"
    return None

def handle_get_user(id):
    user=get_user_by_id(id)
    if not user:
        return"no user found",None
    return None,user

def handle_user_delete(id):
    success=delete_user(id)
    if not success:
        return"cannot delete"
    return None
def handle_user_expense_info():
    users=admin_get_all_users_expense_info()
    if not users:
        return"noo users",None
    return None,users

def handle_admin_user_with_expenses():
    user_expense=admin_get_users_with_expenses()
    if not user_expense:
        return"noo users found",None
    return None,user_expense


def handle_admin_get_users():
    users=admin_get_users()
    if not users:
        return"no users found",None
    return None,users

def handle_edit_profile_username_email(form,id):
    error,username,email=edit_profile_form(form)
    if error:
        return error
    if get_user_by_username_except_current(username,id):
        return "username already exist"
    if get_user_by_email_execpt_curent(email,id):
        return "email already exist"
    
    success=update_user_profile(username,email,id)
    if not success:
        return "username or email already exist"
    return None

def handle_update_password(form,user_id,user):
    error,current_password,new_password=update_password_form(form)
    if error:
        return error
    if not check_password_hash(user["password_hash"],current_password):
        return "current password is invalid"
    new_password_hash=generate_password_hash(new_password)

    success=update_password(user_id,new_password_hash)
    if not success:
        return"unable to update password"
    return None