from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Registration for new users
    if request.method == 'POST':
        name = request.form['name'] 
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_pw = generate_password_hash(password)

        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists.")
            return redirect('/register')

        # Create new user record
        new_user = User(name=name, email=email, password=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered successfully! Please log in.")
        return redirect('/login')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # User login with email and password check
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Store user info in session upon successful login
            session['user_id'] = user.id
            session['role'] = user.role
            session['email'] = user.email
            return redirect('/home')
        flash("Invalid credentials.")
        return redirect('/login')

    return render_template('login.html')

@auth_bp.route('/home')
def home():
    # Home page route that directs users to the dashboard based on their role
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('home.html', email=session['email'], role=session['role'])

@auth_bp.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    return redirect('/login')
