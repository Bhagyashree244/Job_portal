from flask import Flask, redirect, url_for, render_template, session
from models import db
from auth import auth_bp
from jobs import job_bp
from dotenv import load_dotenv
from mail_config import mail
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Email configuration from .env
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == 'True'
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

# Database configuration (currently using SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
mail.init_app(app)

# Register Blueprints for auth and job functionalities
app.register_blueprint(auth_bp)
app.register_blueprint(job_bp)

@app.route('/')
def index():
    # If a user is already logged in, redirect to home dashboard
    if 'user_id' in session:
        return redirect(url_for('auth.home'))
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables 
    app.run(debug=True)
