from flask import Blueprint,render_template,url_for,redirect,session,request
from handlers import handle_total_summary,handle_category_summary,handle_filtering,handle_add_update_expense,handle_get_expense,handle_delete
from decorators import login_required

expense_bp=Blueprint("expense",__name__)
@expense_bp.route("/expense")
@login_required
def expense():

    mode=request.args.get("mode","view").strip()
    page_error=request.args.get("error","").strip()
    name=request.args.get("name")
    category=request.args.get("category")
    min_amount=request.args.get("min_amount")
    max_amount=request.args.get("max_amount")
    result=None
    category_summary=None
    if mode=="view":
        result=handle_total_summary(session.get("user_id"),name,category,min_amount,max_amount)
        category_summary=handle_category_summary(session.get("user_id"),name,category,
                                                 min_amount,max_amount)


    filter_error,expenses=handle_filtering(session.get("user_id"),name,category,min_amount,max_amount)
    if filter_error:
        return render_template("expense.html",error=filter_error)
    return render_template("expense.html",expenses=expenses,error=page_error,mode=mode,result=result,
                           category_summary=category_summary)

@expense_bp.route("/",methods=["POST","GET"])
@login_required
def add_expense():

    mode=request.args.get("mode","add")
    if request.method=="POST":
        error=handle_add_update_expense(mode,request.form,session.get("user_id"),id=None)
        if error:
            return render_template("index.html",error=error,mode=mode)
        return redirect(url_for('expense.expense',mode='view'))
    
    return render_template("index.html",mode=mode)

@expense_bp.route("/update/<int:id>",methods=["POST","GET"])
@login_required
def update(id):
    error,expense=handle_get_expense(session.get("user_id"),id)
    mode=request.args.get("mode","update")
    if error:
        return redirect(url_for("expense.expense",mode=mode,error=error))
    mode=request.args.get("mode","update")

    if request.method=="POST":
        error=handle_add_update_expense(mode,request.form,session.get("user_id"),id)
        if error:
            return render_template("index.html",error=error)
        
        return redirect(url_for('expense.expense',mode=mode))
    return render_template("index.html",mode=mode,expense=expense)

@expense_bp.route("/delete_confirm/<int:id>",methods=["POST","GET"])
@login_required
def delete_confirm(id):
    mode=request.args.get("mode","delete")
    error,expense=handle_get_expense(session.get("user_id"),id)
    if error:
        return redirect(url_for('expense.expense',mode=mode,error=error))
    return render_template("index.html",mode=mode,expense=expense)

@expense_bp.route("/delete/<int:id>",methods=["POST","GET"])
@login_required
def delete(id):
    mode=request.args.get('mode','delete')
    if request.method=="POST":
        error=handle_delete(session.get("user_id"),id)
        if error:
            return redirect(url_for('expense.expense',mode=mode,error=error))
        return redirect(url_for('expense.expense',mode=mode))

    return redirect(url_for('expense.expense',mode=mode))
   