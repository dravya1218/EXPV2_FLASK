import os
import sqlite3
db_name=os.getenv("DB_NAME","finance_tracker.db")

def get_user_connection():
    conn=sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_user_table():
    conn=get_user_connection()
    cursor=conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   email TEXT NOT NULL UNIQUE,
                   password_hash TEXT NOT NULL,
                   role TEXT NOT NULL DEFAULT 'user',
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()

def update_user(email):
    conn=get_user_connection()
    cursor=conn.cursor()
    cursor.execute("""UPDATE users SET role='admin'
                   WHERE email = ?""",(email,))
    conn.commit()
    print(cursor.rowcount)
    conn.close()


def create_expense_table():
    conn=get_user_connection()
    cursor=conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS expenses(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   amount REAL NOT NULL,
                   category TEXT NOT NULL,
                   user_id INTEGER NOT NULL,
                   
                   FOREIGN KEY(user_id)
                   REFERENCES users(id)
                   ON DELETE CASCADE
                   )""")
    
    conn.commit()
    conn.close()

def insert_user(username,email,password):
    conn=get_user_connection()
    cursor=conn.cursor()
    try:
        cursor.execute("""INSERT INTO users(
                   username,email,password_hash)
                   VALUES(?,?,?)""",(username,email,password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()

def insert_expense(name,amount,category,user_id):
    conn=get_user_connection()
    cursor=conn.cursor()
    try:
        cursor.execute("""INSERT INTO expenses(name,amount,category,user_id)
                    VALUES(?,?,?,?)""",(name,amount,category,user_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()




def delet_user(id):
    conn=get_user_connection()
    cursor=conn.cursor()
    try:
        cursor.execute("""DELETE FROM users WHERE id = ?""",(id,))
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_users_email(email):
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE email = ?""",(email,))
    user_email= cursor.fetchone()
    conn.close()
    return user_email

def get_user_username(username):
    conn=get_user_connection()
    cursor=conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE username = ?""",(username,))
    user_username=cursor.fetchone()
    conn.close()
    return user_username

"""HERE WE DONT NEED TO USE 'AND 1=1' BECAUSE WE ALREADY USE WHERE WE ONLY NEED TO USE 'AND 1=1'  
WHEN WE DONT KNOW WHICH NEXT CONDITION WOULD BE FIRST 
BECAUSE THERE WE NEED TO ADD WHERE """ 
def filtering(user_id,name=None,category=None,min_amount=None,max_amount=None):
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
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
    cursor.execute(qurey,values)
    expenses=cursor.fetchall()
    conn.close()
    return expenses

def total_expense_summary(user_id,name=None,category=None,min_amount=None,max_amount=None):
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
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
    cursor.execute(qurey,values)
    result=cursor.fetchone()
    conn.close()
    return result

def total_category_summary(user_id,name=None,category=None,min_amount=None,max_amount=None):
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
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
    cursor.execute(qurey,values)
    category_summary=cursor.fetchall()
    conn.close()
    return category_summary

def get_expense(user_id,id):
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""SELECT * FROM expenses WHERE id = ? AND user_id = ?""",(id,user_id))
    expense=cursor.fetchone()
    conn.close()
    return expense

def update(user_id,id,name,amount,category):
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""UPDATE expenses SET
                   name = ? , amount = ? , category = ?
                   WHERE id = ? AND user_id = ?""",(name,amount,category,id,user_id))
    conn.commit()
    conn.close()
    return True

def delete_expense(user_id,id):
    conn=get_user_connection()
    cursor=conn.cursor()
    cursor.execute(""" DELETE FROM expenses WHERE id = ? AND user_id = ?""",
                   (id,user_id))
    conn.commit()
    conn.close()
    return True


def admin_get_users():
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""SELECT id,username,email,role,created_at
                   FROM users
                   """)
    users=cursor.fetchall()
    conn.close()
    return users

def admin_get_users_with_expenses():
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""SELECT
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
    user_expenses=cursor.fetchall()
    conn.close()
    return user_expenses

def admin_get_all_users_expense_info():
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""SELECT
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
    users=cursor.fetchall()
    conn.close()
    return users

def get_user_by_id(id):
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE id = ?""",(id,))
    users=cursor.fetchone()
    conn.close
    return users

def delete_user(id):
    conn=get_user_connection()
    print("deleting")
    cursor=conn.cursor()
    cursor.execute("""DELETE FROM users WHERE id = ?""",(id,))
    conn.commit()
    print("deleting")
    conn.close()
    return True

def get_user_by_username_except_current(username,id):
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE username = ?
                   AND id != ?""",(username,id))
    user=cursor.fetchone()
    conn.close()
    return user

def get_user_by_email_execpt_curent(email,id):
    conn=get_user_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE email = ?
                   AND id != ?""",(email,id))
    user=cursor.fetchone()
    conn.close()
    return user

def update_user_profile(username,email,id):
    conn=get_user_connection()
    cursor=conn.cursor()
    try:
        cursor.execute("""UPDATE users set username = ?,
                   email = ?
                       WHERE id = ?""",(username,email,id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
        
def update_password(user_id,new_passwod_hash):
    conn=get_user_connection()
    cursor=conn.cursor()
    cursor.execute("""UPDATE users SET password_hash = ?
                   WHERE id = ?""",(new_passwod_hash,user_id))
    conn.commit()
    success=cursor.rowcount==1
    conn.close
    return success

