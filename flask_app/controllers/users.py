from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def log_and_reg():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.register_user(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    # user is not registered in the db
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session["user_id"]
    }
    user = User.get_one_with_posts(data)
    return render_template("dashboard.html", user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 