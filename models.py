from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    # Optional field to store the seeker’s experience (can be updated via profile)
    experience = db.Column(db.Text, nullable=True)
    # Path to the uploaded resume file (PDF)
    resume_path = db.Column(db.String(100), nullable=True)

# Job Model: allows employers to post jobs
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.String(50), nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Field to mark if the job is closed (employer can mark job as closed)
    is_closed = db.Column(db.Boolean, default=False)

# Application Model: allows seekers to apply to jobs
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)
    resume_path = db.Column(db.String(100), nullable=True)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Status can be Pending, Reviewed, Accepted, Rejected
    status = db.Column(db.String(20), default='Pending')

    job = db.relationship("Job", backref="applications")
    user = db.relationship("User", backref="applications")
