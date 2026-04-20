from flask import Flask, render_template, request, redirect, session
from flask import flash
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.urandom(24)


# Database Setup

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              email TEXT UNIQUE,
              password TEXT
        )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS projects (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              description TEXT,
              deparment TEXT,
              github_link TEXT,
              live_link TEXT
            )
        ''')
    conn.commit()
    conn.close()
init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# HOME ---> LOGIN

@app.route("/")
@login_required
def home():
    return render_template("index.html")


# REGISTER ROUTE

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        cpassword = request.form["cpassword"]
        hashed_password = generate_password_hash(password)
        if password != cpassword:
            flash("Passwords do not match!")
            return redirect("/register")
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
        conn.commit()
        conn.close()
        flash("Registration successful!")
        return redirect("/login")
    return render_template("register.html")

# LOGIN ROUTE
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password")
    return render_template("login.html")

# LOGOUT ROUTE
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!")
    return redirect("/login")

# DEPARTMENTS ROUTE
@app.route("/departments")
@login_required
def departments():
    return render_template("department.html")

# DEPARTMENT PROJECTS ROUTE
@app.route("/departments-projects")
@login_required
def department_projects():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = c.fetchall()
    return render_template("department-projects.html", projects=projects)

# UPLOAD ROUTE
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        department = request.form["department"]
        github_link = request.form["github_link"]
        live_link = request.form["live_link"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO projects (title, description, department, github_link, live_link) VALUES (?, ?, ?, ?, ?)",
                  (title, description, department, github_link, live_link))
        conn.commit()
        conn.close()
        flash("Project uploaded successfully!")
        return redirect("/upload")
    return render_template("upload.html")

# After Request Route
@app.after_request
def app_no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# TEAM ROUTE
@app.route("/team")
def team():
    return render_template("team.html")

# About US ROUTE
@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

if __name__ == "__main__":
    app.run(debug=True)