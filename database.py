import os
from pathlib import Path
import libsql_client as sqlite3
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")
db_url=os.getenv("TURSO_DATABASE_URL")
db_token=os.getenv("TURSO_AUTH_TOKEN")

def get_user_connection():
    conn=sqlite3.create_client_sync(url=db_url, auth_token=db_token)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def _row_as_dict(result, row):
    if row is None:
        return None
    return dict(zip(result.columns, row))

def _rows_as_dicts(result):
    return [_row_as_dict(result, row) for row in result.rows]

def _constraint_failure(exc):
    msg = str(exc).upper()
    return "UNIQUE" in msg or "CONSTRAINT" in msg

def create_user_table():
    conn=get_user_connection()
    conn.execute(""" CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   email TEXT NOT NULL UNIQUE,
                   password_hash TEXT NOT NULL,
                   role TEXT NOT NULL DEFAULT 'user',
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.close()

def update_user(email):
    conn=get_user_connection()
    result=conn.execute("""UPDATE users SET role='admin'
                   WHERE email = ?""",(email,))
    print(result.rows_affected)
    conn.close()


def create_expense_table():
    conn=get_user_connection()

    conn.execute("""CREATE TABLE IF NOT EXISTS expenses(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   amount REAL NOT NULL,
                   category TEXT NOT NULL,
                   user_id INTEGER NOT NULL,
                   
                   FOREIGN KEY(user_id)
                   REFERENCES users(id)
                   ON DELETE CASCADE
                   )""")
    
    conn.close()

def insert_user(username,email,password):
    conn=get_user_connection()
    try:
        conn.execute("""INSERT INTO users(
                   username,email,password_hash)
                   VALUES(?,?,?)""",(username,email,password))
        return True
    except Exception as e:
        if _constraint_failure(e):
            return False
        raise

    finally:
        conn.close()

def insert_expense(name,amount,category,user_id):
    conn=get_user_connection()
    try:
        conn.execute("""INSERT INTO expenses(name,amount,category,user_id)
                    VALUES(?,?,?,?)""",(name,amount,category,user_id))
        return True
    except Exception as e:
        if _constraint_failure(e):
            return False
        raise
    finally:
        conn.close()




def delet_user(id):
    conn=get_user_connection()
    try:
        conn.execute("""DELETE FROM users WHERE id = ?""",(id,))
        return True
    except Exception as e:
        if _constraint_failure(e):
            return False
        raise
    finally:
        conn.close()


def get_users_email(email):
    conn=get_user_connection()
    result=conn.execute("""SELECT * FROM users WHERE email = ?""",(email,))
    user_email= _row_as_dict(result, result.rows[0]) if result.rows else None
    conn.close()
    return user_email

def get_user_username(username):
    conn=get_user_connection()
    result=conn.execute("""SELECT * FROM users WHERE username = ?""",(username,))
    user_username=_row_as_dict(result, result.rows[0]) if result.rows else None
    conn.close()
    return user_username

"""HERE WE DONT NEED TO USE 'AND 1=1' BECAUSE WE ALREADY USE WHERE WE ONLY NEED TO USE 'AND 1=1'  
WHEN WE DONT KNOW WHICH NEXT CONDITION WOULD BE FIRST 
BECAUSE THERE WE NEED TO ADD WHERE """ 
def filtering(user_id,name=None,category=None,min_amount=None,max_amount=None):
    conn=get_user_connection()
    qurey="SELECT * FROM expenses WHERE user_id = ?"
    values=[user_id]

    if name:
        qurey+=" AND name LIKE ?"
        values.append(f"%{name}%")
    if category:
        qurey += " AND LOWER(category) = LOWER(?)"
        values.append(category)              
    if min_amount:
        qurey+=" AND amount >= ?"
        values.append(min_amount) 
    if max_amount:
        qurey+=" AND amount <= ?"
        values.append(max_amount)
    print(qurey)
    print(values)
    result=conn.execute(qurey,values)
    expenses=_rows_as_dicts(result)
    conn.close()
    return expenses

def total_expense_summary(user_id,name=None,category=None,min_amount=None,max_amount=None):
    conn=get_user_connection()
    qurey="SELECT SUM(amount) AS total , COUNT(*) AS count FROM expenses WHERE user_id = ?"
    values=[user_id]

    if name:
        qurey+=" AND name LIKE ?"
        values.append(f"%{name}%")
    if category:
        qurey += " AND LOWER(category) = LOWER(?)"
        values.append(category)              
    if min_amount:
        qurey+=" AND amount >= ?"
        values.append(min_amount) 
    if max_amount:
        qurey+=" AND amount <= ?"
        values.append(max_amount)
    result=conn.execute(qurey,values)
    result=_row_as_dict(result, result.rows[0]) if result.rows else None
    conn.close()
    return result

def total_category_summary(user_id,name=None,category=None,min_amount=None,max_amount=None):
    conn=get_user_connection()
    qurey="SELECT category , SUM(amount) AS total  , COUNT(category) AS count FROM expenses WHERE user_id = ?"
    values=[user_id]

    if name:
        qurey+=" AND name LIKE ?"
        values.append(f"%{name}%")
    if category:
        qurey += " AND LOWER(category) = LOWER(?)"
        values.append(category)               
    if min_amount:
        qurey+=" AND amount >= ?"
        values.append(min_amount) 
    if max_amount:
        qurey+=" AND amount <= ?"
        values.append(max_amount)
    qurey+=" GROUP BY CATEGORY"
    result=conn.execute(qurey,values)
    category_summary=_rows_as_dicts(result)
    conn.close()
    return category_summary

def get_expense(user_id,id):
    conn=get_user_connection()
    result=conn.execute("""SELECT * FROM expenses WHERE id = ? AND user_id = ?""",(id,user_id))
    expense=_row_as_dict(result, result.rows[0]) if result.rows else None
    conn.close()
    return expense

def update(user_id,id,name,amount,category):
    conn=get_user_connection()
    conn.execute("""UPDATE expenses SET
                   name = ? , amount = ? , category = ?
                   WHERE id = ? AND user_id = ?""",(name,amount,category,id,user_id))
    conn.close()
    return True

def delete_expense(user_id,id):
    conn=get_user_connection()
    conn.execute(""" DELETE FROM expenses WHERE id = ? AND user_id = ?""",
                   (id,user_id))
    conn.close()
    return True


def admin_get_users():
    conn=get_user_connection()
    result=conn.execute("""SELECT id,username,email,role,created_at
                   FROM users
                   """)
    users=_rows_as_dicts(result)
    conn.close()
    return users

def admin_get_users_with_expenses():
    conn=get_user_connection()
    result=conn.execute("""SELECT
                   e.id,
                   e.name,
                   e.amount,
                   e.category,
                   e.user_id,
                   u.username,
                   u.email 
                   FROM expenses e
                   INNER JOIN users u
                   ON e.user_id=u.id""")
    user_expenses=_rows_as_dicts(result)
    conn.close()
    return user_expenses

def admin_get_all_users_expense_info():
    conn=get_user_connection()
    result=conn.execute("""SELECT
                   u.id,
                   u.username,
                   u.email,
                   u.role,
                   COUNT(e.id) AS expense_count,
                   COALESCE(SUM(e.amount),0) AS total_amount
                   FROM users u
                   LEFT JOIN expenses e
                   ON u.id=e.user_id
                   GROUP BY u.id
                   """)
    users=_rows_as_dicts(result)
    conn.close()
    return users

def get_user_by_id(id):
    conn=get_user_connection()
    result=conn.execute("""SELECT * FROM users WHERE id = ?""",(id,))
    users=_row_as_dict(result, result.rows[0]) if result.rows else None
    conn.close()
    return users

def delete_user(id):
    conn=get_user_connection()
    print("deleting")
    conn.execute("""DELETE FROM users WHERE id = ?""",(id,))
    print("deleting")
    conn.close()
    return True

def get_user_by_username_except_current(username,id):
    conn=get_user_connection()
    result=conn.execute("""SELECT * FROM users WHERE username = ?
                   AND id != ?""",(username,id))
    user=_row_as_dict(result, result.rows[0]) if result.rows else None
    conn.close()
    return user

def get_user_by_email_execpt_curent(email,id):
    conn=get_user_connection()
    result=conn.execute("""SELECT * FROM users WHERE email = ?
                   AND id != ?""",(email,id))
    user=_row_as_dict(result, result.rows[0]) if result.rows else None
    conn.close()
    return user

def update_user_profile(username,email,id):
    conn=get_user_connection()
    try:
        conn.execute("""UPDATE users set username = ?,
                   email = ?
                       WHERE id = ?""",(username,email,id))
        return True
    except Exception as e:
        if _constraint_failure(e):
            return False
        raise
    finally:
        conn.close()
        
def update_password(user_id,new_passwod_hash):
    conn=get_user_connection()
    result=conn.execute("""UPDATE users SET password_hash = ?
                   WHERE id = ?""",(new_passwod_hash,user_id))
    success=result.rows_affected==1
    conn.close()
    return success
