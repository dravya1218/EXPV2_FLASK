# USER REGISTATION SYSTEM
## Purpose
### What it is
A system that allows new users to create an account.
User information is stored in a database.
Each user gets a unique identity.
### Why it exists
Applications need to know who is using them.
Different users should have separate data.
Passwords must be stored securely.
### When to use it
Sign up pages
User-based applications
Authentication systems
- Syntax
    Users Table
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
### Meaning of Each Part
- id INTEGER PRIMARY KEY AUTOINCREMENT
Unique user ID.
Automatically increases.
- username TEXT NOT NULL UNIQUE
Username must exist.
No duplicates allowed.
- email TEXT NOT NULL UNIQUE
Email must exist.
No duplicate emails.
- password_hash TEXT NOT NULL
Stores hashed password.
Never stores raw password.
- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
Saves account creation time automatically.
Example
Simple Example

User enters:

Username: dravya
Email: dravya@gmail.com
Password: mypassword

Database stores:

id: 1
username: dravya
email: dravya@gmail.com
password_hash: scrypt:...
Finance Tracker Example
Dravya registers
↓
Account saved in users table
↓
Later login will identify Dravya
↓
Expenses can belong to Dravya only
How It Works Internally
Registration Flow
User
↓
Register Form
↓
Route
↓
Handler
↓
Validation
↓
Duplicate Checks
↓
Password Hashing
↓
Database Insert
↓
Success Message
↓
Browser
Flask Request Flow
User
↓
Route (/)
↓
handle_registration()
↓
Database Functions
↓
render_template()
↓
Browser

- Memory Rules
Database file contains tables.
Tables contain rows.
Rows contain data.
Never store raw passwords.
Always hash passwords.
Always validate before inserting.
Always check duplicates.
Database is final authority.

# Expense Tracker Usage
app.py

- Responsibility:

Receive requests.
Call handlers.
Return templates.

Example:

error=handle_registration(request.form)
handlers.py

- Responsibility:

Business logic.
Validation.
Duplicate checking.
Password hashing.

Example:

generate_password_hash(password)
database.py

- Responsibility:

Execute SQL queries.
Insert users.
Retrieve users.

Example:

INSERT INTO users
index.html

- Responsibility:

Display registration form.
Show success/error messages.
Database

- Responsibility:

Store users permanently.

Table:

users

- Stores:

id
username
email
password_hash
created_at
- Summary
Registration creates user accounts.
Users are stored in the users table.
PRIMARY KEY uniquely identifies users.
UNIQUE prevents duplicate usernames and emails.
Passwords must be hashed before saving.
Validation happens before insertion.
Database functions only handle SQL.
Handlers contain business logic.
Routes handle requests and responses.
Registration flow is User → Route → Handler → Database → Template → Browser.

# sqlite3.IntegrityError and try-except in insert_user()

## Purpose

### What it is

* `IntegrityError` is an SQLite exception.
* It occurs when a database constraint is violated.
* Commonly triggered by `UNIQUE`, `NOT NULL`, or `PRIMARY KEY` rules.

### Why it exists

* Prevents invalid data from entering the database.
* Protects data integrity.
* Allows Python to handle database errors gracefully.

### When to use it

* Around `INSERT` statements.
* Around `UPDATE` statements that may violate constraints.
* Whenever a database operation can fail.

---

## Syntax

### General Syntax

```python
try:
    # risky code
except SomeError:
    # handle error
finally:
    # cleanup
```

### insert_user() Example

```python
def insert_user(username, email, password_hash):

    conn = get_user_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users
            (username,email,password_hash)
            VALUES(?,?,?)
            """,
            (username,email,password_hash)
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()
```

---

## Example

### Before Insert

Attempt:

```text
username = dravya
email = new@gmail.com
```

### What Happens

SQLite checks:

```text
username UNIQUE?
```

Result:

```text
Already exists
```

SQLite raises:

```python
sqlite3.IntegrityError
```

### Return Value

```python
return False
```

---

## How It Works Internally

### Success Case

```text
try
↓
INSERT
↓
No constraint broken
↓
commit()
↓
return True
↓
finally
↓
close connection
```

### Failure Case

```text
try
↓
INSERT
↓
UNIQUE violated
↓
sqlite3.IntegrityError
↓
except block
↓
return False
↓
finally
↓
close connection
```

---

## Memory Rules

* `try` = attempt operation.
* `except` = handle failure.
* `finally` = always runs.
* Database constraints raise exceptions.
* `IntegrityError` usually means a constraint was violated.

## Related Concepts

* UNIQUE
* PRIMARY KEY
* NOT NULL
* Database Constraints
* INSERT
* Validation
* Error Handling

# Flask Sessions, Cookies, Requests, and Login Flow

## Purpose

### What it is

* Requests are messages sent from the browser to the server.
* Cookies are small pieces of information stored in the browser.
* Sessions allow Flask to remember a user between requests.
* Together they make login systems possible.

### Why it exists

Without sessions:

User logs in
↓
Request ends
↓
Flask forgets user
```

With sessions:

User logs in
↓
Flask remembers user
↓
User stays logged in
```

### When to use it

* Login systems
* Logout systems
* Protected pages
* User-specific applications

---

## Syntax

### Session

Store data:
from flask import Flask,session
app.secret_key="----"
```python
session["user_id"] = user["id"]
session["username"] = user["username"]
```

Read data:

```python
session["user_id"]
```

Safer:

```python
session.get("user_id")
```

Clear all session data:

```python
session.clear()
```

---

### Secret Key

Required for sessions.

```python
app = Flask(__name__)

app.secret_key = "secret_key"
```

---

### What is a Request?

Every time browser asks the server for something:

```text
Browser
↓
Request
↓
Flask
↓
Response
↓
Browser
```

Example:

```text
GET /login
```

or

```text
POST /login
```

---

### What Happens to Variables?

Example:

```python
username = "dravya"
```

Flow:

```text
Request starts
↓
Variable created
↓
Request ends
↓
Variable destroyed
```

Normal variables do not survive.

---

### What is a Cookie?

Cookie is:

```text
Small information
stored in browser
```

Browser stores it.

Example:

```text
Cookie
↓
user_id = 5
```

---

### Session Flow

Step 1:

User logs in.

```text
Email
Password
```

Step 2:

Server checks database.

```sql
SELECT * FROM users
WHERE email = ?
```

Step 3:

Password verified.

```python
check_password_hash(...)
```

Step 4:

Create session.

```python
session["user_id"] = user["id"]
```

Step 5:

Browser stores cookie.

Step 6:

Future requests send cookie automatically.

```text
Request
+
Cookie
```

Step 7:

Flask rebuilds session.

```python
session["user_id"]
```

User remains logged in.

---

## Memory Rules

* HTTP is stateless.
* Every request is independent.
* Normal variables die after request ends.
* Sessions survive across requests.
* Cookies are stored in browser.
* Browser automatically sends cookies with requests.
* Sessions are used for login systems.
* Never store passwords in session.

---

## Common Mistakes

### Thinking Flask Remembers Variables

Wrong:

```text
Flask remembers username variable forever
```

Reality:

```text
Request ends
↓
Variable destroyed
```

---

### Storing Password in Session

Wrong:

```python
session["password"] = password
```

Correct:

```python
session["user_id"] = user["id"]
```

---

### Forgetting Secret Key

Wrong:

```python
app = Flask(__name__)
```

Correct:

```python
app = Flask(__name__)

app.secret_key = "secret"
```

---

### Confusing Database and Session

Database:

```text
Permanent storage
```

Session:

```text
Current login state
```

---

### Future Protected Routes

```python
if "user_id" not in session:
    return redirect(url_for("login"))
```

Purpose:

```text
Only logged-in users can access page
```

---

### Future User-Specific Expenses

Week 3:

```sql
SELECT *
FROM expenses
WHERE user_id = ?
```

Using:

```python
session["user_id"]
```

Purpose:

```text
Show only current user's expenses
```

---

## Summary

* Request is a message from browser to server.
* Every request is independent.
* Normal variables disappear when request ends.
* Cookie is small information stored in browser.
* Browser automatically sends cookies with requests.
* Session allows Flask to remember users.
* Sessions are commonly used after login.
* Database stores permanent user data.
* Session stores current login state.
* User-specific features depend on sessions.

Flask Expense Tracker Notes

Topic: Query Parameters, Error Passing & Variable Overwriting

What We Built

We implemented error handling for update and delete operations.

When a user tries to access:

- Another user's expense
- A non-existent expense

The application redirects back to the expenses page and displays an error message.

---

Concepts Learned

Query Parameters

Used to send small pieces of data through URLs.

Example:

return redirect(
    url_for(
        "expense",
        mode="update",
        error="No expense found"
    )
)

Generated URL:

/expense?mode=update&error=No+expense+found

Purpose:

- Pass information between routes after redirecting.
- Commonly used for filters, search values, page numbers, and messages.

---

request.args

Used to read query parameters.

Example:

error = request.args.get("error", "")

Meaning:

- Read error from URL.
- If error does not exist, use an empty string.

Example:

/expense?error=No+expense+found

Returns:

"No expense found"

---

Error Flow

User:

/update/9

↓

Route:

error = "No expense found"

↓

Redirect:

return redirect(
    url_for(
        "expense",
        mode=mode,
        error=error
    )
)

↓

Expense Route:

page_error = request.args.get("error", "")

↓

Template:

{% if error %}
    <p>{{ error }}</p>
{% endif %}

↓

Browser:

No expense found

---

Variable Overwriting

Bug discovered:

error = request.args.get("error", "")

Later:

error, expenses = handle_filtering(...)

Problem:

The second assignment destroyed the first value.

Before:

error = "No expense found"

After:

error = None

Result:

Error message disappeared.

---

Fix

Use separate variables.

page_error = request.args.get("error", "")

filter_error, expenses = handle_filtering(...)

Benefits:

- Easier debugging
- Clear responsibility
- Prevents accidental overwriting

---

Software Engineering Lesson

One variable should have one responsibility.

Bad:

error

Used for:

- URL errors
- Filtering errors
- Update errors
- Delete errors

Good:

page_error
filter_error
update_error
delete_error

---

Flask Request Flow

Update Route

↓

Redirect

↓

Query Parameters

↓

Expense Route

↓

request.args

↓

Template

↓

Browser

---

Common Mistakes

Mistake 1

request.args.get("error").strip()

Problem:

None.strip()

Crash.

Correct:

request.args.get("error", "").strip()

---

Mistake 2

Overwriting variables.

error = request.args.get("error", "")
error, expenses = handle_filtering(...)

Original value is lost.

---

Mistake 3

Passing error in URL but forgetting to pass it to template.

return render_template(
    "expense.html",
    expenses=expenses
)

Correct:

return render_template(
    "expense.html",
    expenses=expenses,
    error=page_error
)

---

Why This Matters

This is a real debugging problem that happens in production applications.

The bug was not in:

- Database
- SQL
- Handler
- Template

The bug was caused by variable overwriting.

Learning to trace data through:

Route → Redirect → URL → Route → Template

is an important backend development skill.

---

Summary

- Learned query parameters.
- Learned request.args.
- Implemented redirect-based error handling.
- Learned how data travels through URLs.
- Learned variable overwriting bugs.
- Fixed error messages disappearing.
- Improved variable naming.
- Practiced debugging request flow.
- Strengthened understanding of Flask route communication.
- Learned an important software engineering principle: One variable = One responsibility.

# Finance Tracker V2 Notes

## Topic: Database Relationships, Foreign Keys & Referential Integrity

### What We Learned

We learned how databases connect multiple tables together.

Our Finance Tracker now has:

```text
users
↓
expenses
```

where every expense belongs to a specific user.

---

## Parent Table

A parent table contains data that can exist independently.

Example:

```text
users
```

Reason:

A user can exist even if they have no expenses.

Example:

| id | username |
| -- | -------- |
| 1  | dravya   |
| 2  | john     |

---

## Child Table

A child table depends on another table.

Example:

```text
expenses
```

Reason:

Every expense must belong to a user.

Example:

| id | name   | user_id |
| -- | ------ | ------- |
| 1  | Pizza  | 1       |
| 2  | Coffee | 2       |

---

## One-to-Many Relationship

Definition:

```text
One parent record can have many child records.
```

Example:

```text
One User
↓
Many Expenses
```

Example:

| users.id |
| -------- |
| 1        |

| expenses.user_id |
| ---------------- |
| 1                |
| 1                |
| 1                |
| 1                |

Meaning:

```text
User 1 owns many expenses.
```

---

## Foreign Key

Definition:

A foreign key is a column that points to the primary key of another table.

Example:

```sql
FOREIGN KEY(user_id)
REFERENCES users(id)
```

Meaning:

```text
expenses.user_id
must point to
users.id
```

---

## Why Foreign Keys Exist

Without foreign keys:

```text
Expense
↓
user_id = 99
```

could be inserted even if:

```text
User 99 does not exist.
```

Result:

```text
Invalid database data.
```

Foreign keys prevent this.

---

## Referential Integrity

Definition:

```text
Relationships between tables must always remain valid.
```

Rule:

```text
Every expense must belong to a real user.
```

Valid:

| users.id |
| -------- |
| 1        |
| 2        |

| expenses.user_id |
| ---------------- |
| 1                |
| 2                |

Invalid:

| users.id |
| -------- |
| 1        |
| 2        |

| expenses.user_id |
| ---------------- |
| 1                |
| 99               |

Because:

```text
User 99 does not exist.
```

---

## Orphan Records

Definition:

A child record whose parent record no longer exists.

Example:

User deleted:

| users |
| ----- |
| Empty |

Expenses remain:

| id | name  | user_id |
| -- | ----- | ------- |
| 1  | Pizza | 1       |

Problem:

```text
Expense exists
User does not exist
```

This is an orphan record.

---

## ON DELETE CASCADE

Purpose:

Automatically remove child records when parent records are deleted.

Example:

Delete:

```text
User 1
```

Automatically delete:

```text
All expenses with user_id = 1
```

Result:

No orphan records.

---

## Why We Use IDs Instead Of Usernames

Bad:

```sql
REFERENCES users(username)
```

Problems:

* Username can change.
* Username is not the official row identity.

Good:

```sql
REFERENCES users(id)
```

Reasons:

* Stable
* Unique
* Primary Key
* Never changes

---

## SQLite Foreign Key Syntax

```sql
CREATE TABLE expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    user_id INTEGER NOT NULL,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);
```

---

## Understanding The Syntax

### user_id INTEGER NOT NULL

Meaning:

```text
Every expense must belong to a user.
```

---

### FOREIGN KEY(user_id)

Meaning:

```text
user_id is the foreign key column.
```

---

### REFERENCES users(id)

Meaning:

```text
Check that user_id exists inside users.id.
```

---

### ON DELETE CASCADE

Meaning:

```text
Delete parent
↓
Automatically delete children
```

---

## PRAGMA foreign_keys = ON

SQLite disables foreign key enforcement by default.

Must be enabled:

```python
def get_connection():
    conn = sqlite3.connect("finance_tracker.db")

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn
```

Reason:

```text
Every database connection should enforce foreign keys.
```

---

## Real Finance Tracker Relationship

```text
users
│
├── id
├── username
├── email
└── password_hash

expenses
│
├── id
├── name
├── amount
├── category
└── user_id
```

Relationship:

```text
expenses.user_id
↓
users.id
```

---

## Key Software Engineering Lessons

### One User

Can have:

```text
Many Expenses
```

---

### One Expense

Can belong to:

```text
One User
```

---

### Child Records

Should never point to non-existent parents.

---

### Database Relationships

Must remain valid at all times.

---

## Summary

* Learned Parent Table.
* Learned Child Table.
* Learned One-to-Many Relationships.
* Learned Foreign Keys.
* Learned Referential Integrity.
* Learned Orphan Records.
* Learned ON DELETE CASCADE.
* Learned why IDs are used instead of usernames.
* Learned SQLite foreign key syntax.
* Learned PRAGMA foreign_keys = ON.
* Connected database theory directly to Finance Tracker V2.


# SQL Joins Notes

Purpose:
SQL Joins are used to combine data from multiple tables based on a relationship.

Without joins:
- users table is separate
- expenses table is separate

With joins:
- We can display expense information together with user information.

--------------------------------------------------

Tables Used

users

id
username
email

expenses

id
name
amount
category
user_id

Relationship:

users.id
     ↑
expenses.user_id

One User → Many Expenses

--------------------------------------------------

INNER JOIN

Definition:

Returns only matching rows from both tables.

Syntax:

SELECT *
FROM expenses
INNER JOIN users
ON expenses.user_id = users.id

Meaning:

Take an expense only if its user exists.

--------------------------------------------------

Example

Users:

1 Dravya
2 Parth

Expenses:

Pizza user_id = 1
Petrol user_id = 1
Travel user_id = 99

Result:

Dravya Pizza
Dravya Petrol

Travel does NOT appear because user_id 99 does not exist.

--------------------------------------------------

Real Project Example

SELECT
    e.name,
    e.amount,
    u.username
FROM expenses e
INNER JOIN users u
ON e.user_id = u.id

Output:

Pizza   100   Dravya
Petrol  200   Dravya
Travel  300   Parth

--------------------------------------------------

LEFT JOIN

Definition:

Returns ALL rows from the left table.

If no matching row exists in the right table,
NULL values are returned.

Syntax:

SELECT *
FROM users
LEFT JOIN expenses
ON users.id = expenses.user_id

--------------------------------------------------

Example

Users:

Dravya
Parth
John

Expenses:

Dravya → Pizza
Parth → Travel

Result:

Dravya Pizza
Parth Travel
John NULL

John appears even though he has no expenses.

--------------------------------------------------

INNER JOIN vs LEFT JOIN

INNER JOIN

Returns:
Only matching rows

Example:
Users with expenses only

--------------------------------------------------

LEFT JOIN

Returns:
All rows from left table

Example:
All users, even if they have no expenses

--------------------------------------------------

Aliases

Purpose:

- Shorter queries
- Cleaner code
- Easier to read

Without Alias:

SELECT users.username,
       expenses.name
FROM expenses
INNER JOIN users
ON expenses.user_id = users.id

--------------------------------------------------

With Alias:

SELECT u.username,
       e.name
FROM expenses e
INNER JOIN users u
ON e.user_id = u.id

Meaning:

u = users
e = expenses

--------------------------------------------------

Alias Rules

Table Alias:

users u
expenses e

Column Access:

u.username
u.email

e.name
e.amount
e.category

--------------------------------------------------

Selecting Specific Columns

SELECT
    e.id,
    e.name,
    e.amount,
    e.category,
    u.username,
    u.email
FROM expenses e
INNER JOIN users u
ON e.user_id = u.id

Purpose:

Only fetch required columns.

--------------------------------------------------

Selecting All Columns

SELECT *
FROM expenses e
INNER JOIN users u
ON e.user_id = u.id

Problem:

Returns all columns including:

expenses.id
expenses.user_id
users.id

Can become confusing.

Prefer selecting specific columns.

--------------------------------------------------

Project Usage

User Expense Page:

Uses:

WHERE user_id = ?

Purpose:

Show only current user's expenses.

--------------------------------------------------

Admin Expense Page:

Uses:

INNER JOIN

Purpose:

Show:

Expense Name
Amount
Category
Username
Email

for every expense.

--------------------------------------------------

Key Concepts

JOIN
Combines data from multiple tables.

INNER JOIN
Returns matching rows only.

LEFT JOIN
Returns all rows from left table.

ON
Defines join condition.

Alias
Short name for table.

u
users table alias.

e
expenses table alias.

expenses.user_id
Foreign key.

users.id
Primary key.

Relationship:

users.id = expenses.user_id

--------------------------------------------------

Quick Summary

One User → Many Expenses

expenses.user_id references users.id

INNER JOIN:
Only matching rows

LEFT JOIN:
All rows from left table

Aliases:
u = users
e = expenses

ON clause:
Defines relationship between tables

Joins allow data from multiple tables to be displayed together.

--------------------------------------------------

Admin System Debugging Lessons

Problem:

update_user("email")

was returning:

0

Meaning:

No rows were updated.

Initial Wrong Assumption:

Thought:
- SQL query wrong
- users table missing
- role column issue

Actual Cause:

Email in WHERE clause did not match any user row.

Lesson:

rowcount = 0

means:

Query executed successfully
BUT no matching row found.

--------------------------------------------------

Debugging Strategy

Step 1

Verify table exists.

Query:

SELECT name
FROM sqlite_master
WHERE type='table'

Result:

users
sqlite_sequence

Meaning:

Table exists.

--------------------------------------------------

Step 2

Verify users exist.

Query:

SELECT *
FROM users

Purpose:

Check actual data.

--------------------------------------------------

Step 3

Verify exact email.

Problem:

UPDATE uses:

WHERE email = ?

Email must exactly match database value.

Even one wrong character:

0 rows updated.

--------------------------------------------------

Step 4

Verify update worked.

Before:

role = user

Run:

UPDATE users
SET role='admin'
WHERE email=?

After:

role = admin

Confirmed update succeeded.

--------------------------------------------------

Temporary Database Testing

Created temporary functions:

show_users()

Purpose:

Inspect database contents.

Used only for debugging.

Important:

Temporary testing code should be removed after debugging is finished.

Keep:

Functions

Remove:

Function calls at bottom of file.

--------------------------------------------------

Database vs Code

Important Lesson:

Sometimes code is correct.

Problem is data.

Always verify:

1. Table exists
2. Row exists
3. Query matches row

before changing code.

--------------------------------------------------

Real Software Engineering Lesson

When debugging:

Do not guess.

Verify:

Database
↓
Data
↓
Query
↓
Code

in that order.

Most bugs are solved faster by checking actual data than by rewriting code.
# COALESCE()
- is usded to replace null with a value you choose
suppose

- SQL 
SELECT u.username,SUM(e.amount) FROM users u LEFT JOIN expenses e
ON u.id=e.user_id
GROUP BY u.id
- DATA
dravya -> 100+200
parth -> 300
john - > no expenses
- RESULT
dravya 300
parth 300
john NULL

because sum of no rows returns NULL

- using COALESCE
SELECT u.username,
COALESCE(SUM(e.amount),0) FROM users u LEFT JOIN expenses e
ON u.id=e.user_id
GROUP BY u.id
- result
DRAVYA 300
PARTH 300
JOHN 0

- meaning
COALESCE(VALUE,REPLACEMENT)
if value is NULL -> use replacement

# Finance Tracker V2 Notes

## Topic: Admin System & Authorization

--------------------------------------------------

Role-Based Access Control (RBAC)

Purpose:

Different users can have different permissions.

Example:

admin
user

Admin can:

- View all users
- View all expenses
- Delete users

Normal users cannot.

--------------------------------------------------

Role Column

Added to users table:

role TEXT NOT NULL DEFAULT 'user'

Purpose:

Store what type of user is logged in.

Examples:

user
admin

--------------------------------------------------

Making A User Admin

Update query:

UPDATE users
SET role='admin'
WHERE email=?

Purpose:

Promote existing user to admin.

--------------------------------------------------

rowcount

Purpose:

Check how many rows were affected.

Example:

print(cursor.rowcount)

Output:

1

Meaning:

One row updated successfully.

Output:

0

Meaning:

No matching row found.

--------------------------------------------------

Session Role Storage

After successful login:

session["user_id"] = user["id"]
session["role"] = user["role"]

Purpose:

Store user permissions.

Now Flask remembers:

- Who is logged in
- What role they have

--------------------------------------------------

Authorization vs Authentication

Authentication

Question:

"Who are you?"

Examples:

Login
Password verification

--------------------------------------------------

Authorization

Question:

"What are you allowed to do?"

Examples:

Admin page access
Delete users
View all users

--------------------------------------------------

Admin Check Function

def is_admin():
    return session.get("role") == "admin"

Purpose:

Check whether current user is admin.

Returns:

True
False

--------------------------------------------------

Admin Route Protection

Pattern:

if not is_logged_in():
    redirect(login)

if not is_admin():
    redirect(expense)

Purpose:

Prevent normal users from accessing admin pages.

--------------------------------------------------

Admin Users Page

Purpose:

Display all registered users.

Data displayed:

id
username
email
role
created_at

Learned:

SELECT multiple columns
Displaying database records in table

--------------------------------------------------

created_at

Column:

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Purpose:

Automatically store registration time.

Example:

2026-06-15 09:30:15

Important Lesson:

Column name is:

created_at

Not:

create_at

--------------------------------------------------

Admin Expenses Page

Purpose:

Display:

Expense
Amount
Category
Username
Email

for every expense.

Uses:

INNER JOIN

Query combines:

expenses table
users table

--------------------------------------------------

Delete Confirmation Page

Pattern:

GET
→ Show confirmation page

POST
→ Actually delete

Purpose:

Prevent accidental deletion.

--------------------------------------------------

Single Route Delete Pattern

One route handles:

GET
POST

Example Flow:

GET
↓
Show confirmation

POST
↓
Delete user
↓
Redirect

Cleaner than multiple routes.

--------------------------------------------------

Cascade Delete Tested

Delete User
↓
User removed
↓
All related expenses removed automatically

Reason:

ON DELETE CASCADE

Important Understanding:

Application deletes user.

SQLite automatically deletes child expenses.

--------------------------------------------------

Debugging Lessons

1.

If rowcount = 0

Check:

- User exists?
- Email matches?

--------------------------------------------------

2.

If dict(row) fails

Check:

conn.row_factory = sqlite3.Row

--------------------------------------------------

3.

If no such table error appears

Check:

- Correct database file
- Table creation function executed

--------------------------------------------------

Key Software Engineering Lessons

Authentication
=
Identity

Authorization
=
Permission

Role
=
Permission Level

Admin routes must always be protected.

Database relationships can enforce business rules automatically.

Delete confirmation should use POST, not GET.

Sessions can store both:

user_id
role

--------------------------------------------------

Admin System Debugging Lessons

Problem:

update_user("email")

was returning:

0

Meaning:

No rows were updated.

Initial Wrong Assumption:

Thought:
- SQL query wrong
- users table missing
- role column issue

Actual Cause:

Email in WHERE clause did not match any user row.

Lesson:

rowcount = 0

means:

Query executed successfully
BUT no matching row found.

--------------------------------------------------

Debugging Strategy

Step 1

Verify table exists.

Query:

SELECT name
FROM sqlite_master
WHERE type='table'

Result:

users
sqlite_sequence

Meaning:

Table exists.

--------------------------------------------------

Step 2

Verify users exist.

Query:

SELECT *
FROM users

Purpose:

Check actual data.

--------------------------------------------------

Step 3

Verify exact email.

Problem:

UPDATE uses:

WHERE email = ?

Email must exactly match database value.

Even one wrong character:

0 rows updated.

--------------------------------------------------

Step 4

Verify update worked.

Before:

role = user

Run:

UPDATE users
SET role='admin'
WHERE email=?

After:

role = admin

Confirmed update succeeded.

--------------------------------------------------

Temporary Database Testing

Created temporary functions:

show_users()

Purpose:

Inspect database contents.

Used only for debugging.

Important:

Temporary testing code should be removed after debugging is finished.

Keep:

Functions

Remove:

Function calls at bottom of file.

--------------------------------------------------

Database vs Code

Important Lesson:

Sometimes code is correct.

Problem is data.

Always verify:

1. Table exists
2. Row exists
3. Query matches row

before changing code.

--------------------------------------------------

Real Software Engineering Lesson

When debugging:

Do not guess.

Verify:

Database
↓
Data
↓
Query
↓
Code

in that order.

Most bugs are solved faster by checking actual data than by rewriting code.

# Flask Decorators Notes

--------------------------------------------------

What Is A Decorator?

A decorator is a function that adds extra behavior to another function without modifying the original function.

Purpose:

- Reuse code
- Avoid repetition
- Separate responsibilities

--------------------------------------------------

Problem Without Decorators

Example:

@app.route("/expenses")
def expenses():

    if not is_logged_in():
        return redirect(...)

Every protected route contains:

if not is_logged_in()

Repeated many times.

Problems:

- Code duplication
- Harder maintenance
- Easy to forget protection

--------------------------------------------------

Decorator Solution

Write login logic once.

Apply everywhere.

Example:

@login_required
def expenses():

Now every route automatically gets login protection.

--------------------------------------------------

Functions Are Objects

Functions can be:

- Stored in variables
- Passed as arguments
- Returned from functions

Example:

def hello():
    print("Hello")

x = hello

x()

Output:

Hello

--------------------------------------------------

Functions Can Be Passed As Arguments

def hello():
    print("Hello")

def execute(func):
    func()

execute(hello)

Output:

Hello

--------------------------------------------------

Function Inside Function

def outer():

    def inner():
        print("Hello")

    return inner

Purpose:

Create a new function dynamically.

--------------------------------------------------

Basic Decorator Structure

def decorator(func):

    def wrapper():
        print("Before")

        func()

        print("After")

    return wrapper

--------------------------------------------------

What Is func?

func represents the original function.

Example:

decorator(hello)

Then:

func = hello

--------------------------------------------------

What Is wrapper?

wrapper is the new function.

Purpose:

Add extra behavior before and after the original function.

Example:

Before
↓
Original Function
↓
After

--------------------------------------------------

Why Return wrapper?

Correct:

return wrapper

Wrong:

return func

Reason:

We want the wrapper to run.

If we return func:

Extra behavior is lost.

--------------------------------------------------

Decorator Flow

def hello():
    print("Hello")

hello = decorator(hello)

Process:

hello
↓
passed to decorator
↓
wrapper created
↓
wrapper returned
↓
hello now points to wrapper

--------------------------------------------------

What Happens To Original Function?

Original function is NOT destroyed.

wrapper keeps a reference to it.

Example:

wrapper
 ├─ Before
 ├─ func → original hello
 └─ After

--------------------------------------------------

Decorator Shortcut Syntax

This:

def hello():
    pass

hello = decorator(hello)

is identical to:

@decorator
def hello():
    pass

--------------------------------------------------

Important Understanding

Decorator does NOT call wrapper.

Decorator:

- Creates wrapper
- Returns wrapper

Flask later calls wrapper.

--------------------------------------------------

Flask Login Decorator

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not is_logged_in():
            return redirect(url_for("user_login"))

        return func(*args, **kwargs)

    return wrapper

Purpose:

Protect routes.

--------------------------------------------------

Decorator Execution Timing

Decorator runs:

Once when application starts.

Wrapper runs:

Every request.

Important:

Decorator creates wrapper.

Wrapper handles requests.

--------------------------------------------------

Why Use *args and **kwargs?

Some routes have arguments.

Example:

@app.route("/update/<int:id>")
def update(id):

Flask calls:

update(5)

Since wrapper is now being called:

wrapper(5)

wrapper must accept arguments.

--------------------------------------------------

Meaning Of *args

Collect positional arguments.

Example:

wrapper(5)

args:

(5,)

--------------------------------------------------

Meaning Of **kwargs

Collect keyword arguments.

Example:

wrapper(id=5)

kwargs:

{"id": 5}

--------------------------------------------------

Why Pass Them To func?

return func(*args, **kwargs)

Purpose:

Forward original arguments to original route.

Example:

wrapper(5)
↓
func(5)
↓
update(5)

--------------------------------------------------

Why Does Wrapper Receive Arguments?

Because Flask calls wrapper.

Not the decorator.

Flow:

User visits:

/update/5

Flask:

wrapper(5)

wrapper:

func(5)

original route:

update(5)

--------------------------------------------------

What Does @wraps Do?

Without @wraps:

Function metadata is lost.

Example:

hello.__name__

returns:

wrapper

--------------------------------------------------

With @wraps

hello.__name__

returns:

hello

Purpose:

Preserve original function information.

Used for:

- Debugging
- Error messages
- Documentation

Important:

Decorator works without @wraps.

@wraps only preserves metadata.

--------------------------------------------------

Why Decorators Exist

1.

Avoid code duplication.

Without decorator:

20 routes
↓
20 login checks

With decorator:

20 routes
↓
1 login decorator

--------------------------------------------------

2.

Keep responsibilities separate.

expense()

should focus on:

Showing expenses

Not:

- Login checks
- Authorization checks
- Redirect logic

--------------------------------------------------

3.

Add behavior without modifying original function.

Decorator acts like a layer:

Request
↓
Decorator
↓
Original Function

--------------------------------------------------

Admin Decorator

Pattern:

def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not is_admin():
            return redirect(url_for("expense"))

        return func(*args, **kwargs)

    return wrapper

Purpose:

Allow only admins to access protected routes.

--------------------------------------------------

Key Lessons

Decorator
=
Function that returns another function.

func
=
Original function.

wrapper
=
New function that adds behavior.

return wrapper
=
Replace original function with wrapper.

Decorator runs once.

Wrapper runs every request.

*args and **kwargs
=
Allow wrapper to work with any route arguments.

@wraps
=
Preserves original function metadata.

Decorators reduce repetition and improve code organization.

# Flask Decorators Notes (Part 2)

--------------------------------------------------

Most Important Decorator Insight

Decorator does NOT call wrapper.

Decorator:

- Creates wrapper
- Returns wrapper

Flask later calls wrapper.

--------------------------------------------------

Why Wrapper Exists

Without wrapper:

def decorator(func):

    print("Before")
    func()
    print("After")

Problem:

func() runs immediately when decorator executes.

This happens during application startup.

Not when the route is requested.

--------------------------------------------------

Purpose Of Wrapper

Wrapper delays execution.

Instead of:

Decorator
↓
Immediately run function

We get:

Decorator
↓
Create wrapper
↓
Return wrapper
↓
Wait for request
↓
Run wrapper
↓
Run original function

--------------------------------------------------

Execution Timeline

Application Startup

update = login_required(update)

Decorator executes once.

Decorator creates wrapper.

Decorator returns wrapper.

update now points to wrapper.

--------------------------------------------------

Request Time

User visits:

/update/5

Flask calls:

wrapper(5)

Wrapper executes.

Login check runs.

If login succeeds:

func(5)

Original route executes.

--------------------------------------------------

Decorator Runs Once

Decorator:

login_required(update)

Runs once when application starts.

--------------------------------------------------

Wrapper Runs Every Request

Every time user visits:

/expenses
/profile
/update/5

Wrapper executes.

--------------------------------------------------

Understanding Route Arguments

Route:

@app.route("/update/<int:id>")
def update(id):

User visits:

/update/5

Flask extracts:

id = 5

--------------------------------------------------

After Decoration

update
↓
wrapper

Flask calls:

wrapper(5)

Not:

login_required(5)

Not:

update(5)

--------------------------------------------------

Why Wrapper Uses *args and **kwargs

Wrapper must accept any route arguments.

Examples:

wrapper()

wrapper(5)

wrapper(5,10)

wrapper(id=5)

--------------------------------------------------

Meaning Of *args

Stores positional arguments.

Example:

wrapper(5)

args

(5,)

--------------------------------------------------

Meaning Of **kwargs

Stores keyword arguments.

Example:

wrapper(id=5)

kwargs

{"id": 5}

--------------------------------------------------

Why Pass Arguments To func

Wrapper receives route arguments.

Original route still needs them.

Example:

wrapper(5)

↓

func(5)

↓

update(5)

--------------------------------------------------

What Happens Without *args And **kwargs

Wrapper:

def wrapper():

Route:

def update(id):

Flask:

wrapper(5)

Error:

wrapper() takes 0 positional arguments
but 1 was given

--------------------------------------------------

Why Return func(*args, **kwargs)

Purpose:

Run original function and return its result.

Example:

def update(id):
    return f"Updating {id}"

Wrapper:

return func(5)

Original route returns:

Updating 5

Wrapper returns:

Updating 5

Flask receives:

Updating 5

--------------------------------------------------

Without Return

func(5)

Original function runs.

But wrapper returns:

None

Flask receives:

None

Usually causes an error.

--------------------------------------------------

Difference Between Two Returns

1.

return wrapper

Purpose:

Return the new function.

Replace original function.

--------------------------------------------------

2.

return func(*args, **kwargs)

Purpose:

Run original function.

Return original function's result.

--------------------------------------------------

Mental Model

Decorator
↓
Creates wrapper
↓
Returns wrapper
↓
Original function name points to wrapper

Request
↓
Wrapper executes
↓
Checks condition
↓
Calls original function
↓
Returns original result
↓
Flask receives result

--------------------------------------------------

Real Login Decorator Flow

User requests:

/expenses

↓

wrapper()

↓

is_logged_in()

↓

False

↓

redirect(login)

Original route never executes.

--------------------------------------------------

Logged In Flow

User requests:

/expenses

↓

wrapper()

↓

is_logged_in()

↓

True

↓

func()

↓

expenses()

↓

render_template(...)

↓

Flask displays page

--------------------------------------------------

Biggest Lessons

Decorator runs once.

Wrapper runs every request.

Wrapper delays execution of original function.

Wrapper receives route arguments.

Wrapper forwards arguments to original function.

return wrapper
=
return new function

return func(...)
=
return original function result

Decorators allow behavior to be added without modifying the original route.

Examples:

Login checking
Admin checking
Permission checking
Logging
Caching
Timing

# Flask Blueprints Notes

--------------------------------------------------

What Problem Do Blueprints Solve?

As projects grow:

app.py becomes very large.

Example:

app.py

- login
- signup
- logout

- add_expense
- update_expense
- delete_expense

- admin_users
- admin_expenses
- admin_delete_user

500+ lines

Problems:

- Hard to find code
- Hard to maintain
- Hard to understand

--------------------------------------------------

Purpose Of Blueprints

Blueprints organize routes into logical groups.

Examples:

auth.py
expense.py
admin.py

Each file contains related routes.

--------------------------------------------------

Blueprint Mental Model

Blueprint
=
Container of routes

Example:

auth_bp

contains:

/login
/signup
/logout

--------------------------------------------------

Before Blueprints

@app.route("/login")
def login():

@app.route("/expenses")
def expenses():

Routes are registered directly into Flask app.

--------------------------------------------------

How Flask Stores Routes Without Blueprints

When Flask sees:

@app.route("/login")

it immediately stores:

/login → login function

When Flask sees:

@app.route("/expenses")

it immediately stores:

/expenses → expenses function

Routes go directly into Flask app.

--------------------------------------------------

Creating A Blueprint

from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

Meaning:

Create a blueprint called auth.

--------------------------------------------------

Route Inside Blueprint

Instead of:

@app.route("/login")

Use:

@auth_bp.route("/login")

Meaning:

This route belongs to auth blueprint.

--------------------------------------------------

Where Is Route Stored?

Example:

@auth_bp.route("/login")
def login():

Route is stored inside:

auth_bp

NOT inside:

app

--------------------------------------------------

Important Understanding

After writing:

@auth_bp.route("/login")

Flask app still does NOT know about /login.

Only blueprint knows about it.

Mental Model:

Flask App
(empty)

auth_bp
└── /login

--------------------------------------------------

Blueprint Registration

In app.py:

from auth import auth_bp

app.register_blueprint(auth_bp)

Purpose:

Tell Flask about routes inside blueprint.

--------------------------------------------------

What register_blueprint Does

Before:

auth_bp
├── /login
├── /signup
└── /logout

Flask App
(empty)

--------------------------------------------------

After:

app.register_blueprint(auth_bp)

Flask App
├── /login
├── /signup
└── /logout

Now Flask knows these routes exist.

--------------------------------------------------

Without Registration

If you forget:

app.register_blueprint(auth_bp)

Then:

/login

returns:

404 Not Found

Reason:

Flask never learned that route exists.

--------------------------------------------------

Blueprint Route Flow

Create Blueprint

↓

Add Routes To Blueprint

↓

Register Blueprint

↓

Flask Copies Routes Into App

↓

Routes Become Available

--------------------------------------------------

Blueprint Structure Example

routes/

├── auth.py
│   ├── login()
│   ├── signup()
│   └── logout()

├── expense.py
│   ├── add_expense()
│   ├── update_expense()
│   └── delete_expense()

└── admin.py
    ├── admin_users()
    ├── admin_expenses()
    └── admin_delete_user()

--------------------------------------------------

Main Benefit

Not faster execution.

Not better database performance.

Purpose:

Better project organization.

--------------------------------------------------

Key Lessons

Blueprint
=
Container of routes

@app.route()
=
Register directly into Flask app

@auth_bp.route()
=
Store route inside blueprint

app.register_blueprint(...)
=
Tell Flask to import blueprint routes

Without registration:
404 Not Found

Blueprints help developers organize large Flask projects.

Blueprint Lesson

Problem:
As app.py grows, routes become difficult to manage.

Solution:
Blueprints allow routes to be grouped by responsibility.

Example:
auth.py
    login
    signup
    logout

admin.py
    admin users
    admin expenses
    admin summary

expense.py
    expense routes

Key Concepts:

1. Create Blueprint

auth_bp = Blueprint("auth", __name__)

2. Use Blueprint Route

@auth_bp.route("/login")

instead of

@app.route("/login")

3. Register Blueprint

app.register_blueprint(auth_bp)

4. Endpoint Names

Before:
url_for("user_login")

After:
url_for("auth.user_login")

Format:
url_for("blueprint_name.function_name")

5. Shared Code

When multiple blueprints need decorators:

decorators.py

contains:
login_required
admin_required
is_logged_in
is_admin

6. Common Bug

Handler must always return:

return error, data

not

return data, error

Otherwise variables get swapped.