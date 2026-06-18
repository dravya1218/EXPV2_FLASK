def user_sign_up_form(form):
    username=form.get("username","").strip()
    email=form.get("email","").strip()
    password=form.get("password","").strip()
    if username=="":
        return "username canot be empty",None,None,None
    if email=="":
        return"email cannot be empty",None,None,None
    if password=="":
        return"password cannot be empty",None,None,None
    return None,username,email,password

def user_login_form(form):
    email=form.get("email","").strip()
    password=form.get("password","").strip()
    if email=="":
        return"email cannot be empty",None,None
    if password=="":
        return"password cannot be empty",None,None
    return None,email,password

def add_expense_form(form):
    name=form.get("name","").strip()
    amount=form.get("amount","").strip()
    category=form.get("category","").strip()
    if name=="":
        return"name cannot be empty",None,None,None
    if name.isdigit():
        return "Name cannot be all digits",None,None,None

    if len(name) < 2:
        return "Name must be at least 2 characters",None,None,None

    if len(name) > 50:
        return "Name cannot be more than 50 characters",None,None,None

    if amount=="":
        return"amount cannot be empty",None,None,None
    if "."in amount:
        part=amount.split(".")
        if len(part[1])>2:
            return "Maximum 2 decimal places allowed",None,None,None
    try:
        amount=float(amount)
        if amount <= 0:
            return "Amount must be greater than 0",None,None,None

        if amount > 1000000:
            return "Amount is too large",None,None,None
    except ValueError:
        return "amount must be an real number",None,None,None
    
    if category=="":
        return"category cannot be empty",None,None,None
    return None,name,amount,category

def edit_profile_form(form):
    username=form.get("username","").strip()
    email=form.get("email","").strip()
    if username=="":
        return "username cannot be empty",None,None
    if username.isdigit():
        return"username cannot be all digit",None,None
    if email=="":
        return "email cannot be empty",None,None
    return None,username,email

def update_password_form(form):
    current_pass=form.get("current_password").strip()
    new_pass=form.get("new_password").strip()
    confirm_pass=form.get("confirm_password").strip()
    if not current_pass or not new_pass or not confirm_pass:
        return"all fileds are required",None,None
    if new_pass==current_pass:
        return"new password cannot be same as old password",None,None
    if new_pass != confirm_pass:
        return"new password and confirm password doesnt match",None,None
    if len(new_pass)<6:
        return"password must be atleast 6 characters",None,None
    return None,current_pass,new_pass