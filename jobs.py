from flask import Blueprint, render_template, request, redirect, session, flash, url_for, current_app
from models import db, Job, Application, User
from werkzeug.utils import secure_filename
from flask_mail import Message
from mail_config import mail
import os
from datetime import datetime

job_bp = Blueprint('job', __name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    # Check if the uploaded file has an allowed extension (PDF)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@job_bp.route('/post-job', methods=['GET', 'POST'])
def post_job():
    # Route for employers to post a new job
    if 'user_id' not in session or session['role'] != 'employer':
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        job_type = request.form['job_type']
        salary = request.form['salary']

        # Create a new job instance with default is_closed = False
        job = Job(title=title, description=description, location=location,
                  job_type=job_type, salary=salary, posted_by=session['user_id'])
        db.session.add(job)
        db.session.commit()
        flash("Job posted successfully!")
        return redirect('/jobs')

    return render_template('post_job.html')

@job_bp.route('/jobs')
def job_list():
    # Route to list all jobs with pagination and search query support
    # Pagination: Show 5 jobs per page
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', '')
    if query:
        # Search job title (case-insensitive search)
        jobs_query = Job.query.filter(Job.title.ilike(f'%{query}%'))
    else:
        jobs_query = Job.query

    # Order jobs by date added (if you add such a field, here we use id as a proxy)
    pagination = jobs_query.order_by(Job.id.desc()).paginate(page=page, per_page=5, error_out=False)

    jobs = pagination.items
    return render_template('job_list.html', jobs=jobs, pagination=pagination, query=query)

@job_bp.route('/search')
def search_jobs():
    # A simple search route; alternatively, the job_list route now accepts a query parameter
    return redirect(url_for('job.job_list', q=request.args.get('q', '')))

@job_bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    # Route for job seekers to apply for a job
    if 'user_id' not in session or session['role'] != 'seeker':
        return redirect('/login')

    job = Job.query.get_or_404(job_id)

    if request.method == 'POST':
        cover_letter = request.form['cover_letter']
        resume = request.files.get('resume')

        resume_path = None
        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            resume.save(path)
            resume_path = path

        # Create a new Application record with status 'Pending'
        application = Application(job_id=job_id, user_id=session['user_id'],
                          cover_letter=cover_letter, resume_path=resume_path)
        db.session.add(application)
        db.session.commit()

        # Send confirmation email using Flask-Mail
        msg = Message(
            subject="Job Application Confirmation",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[session['email']],
            body=f"""Dear {session['email']},

You have successfully applied for '{job.title}'.

We will review your application shortly.

Regards,
Job Portal Team
"""
        )
        mail.send(msg)

        flash("Applied successfully! A confirmation email was sent.")
        return redirect('/dashboard/seeker')

    return render_template('apply_job.html', job=job)

@job_bp.route('/dashboard/employer')
def employer_dashboard():
    # Dashboard for employers showing posted jobs and number of applications per job
    if 'user_id' not in session or session['role'] != 'employer':
        return redirect('/login')

    jobs = Job.query.filter_by(posted_by=session['user_id']).all()
    job_data = []
    for job in jobs:
        applicant_count = Application.query.filter_by(job_id=job.id).count()
        job_data.append({"id": job.id, "title": job.title, "applicant_count": applicant_count, "is_closed": job.is_closed})
    return render_template('dashboard_employer.html', jobs=job_data)


@job_bp.route('/dashboard/seeker')
def dashboard_seeker():
     # Dashboard for job seekers displaying applied jobs with current status
    if 'user_id' not in session or session['role'] != 'seeker':
        return redirect('/login')
    
    user = User.query.get(session['user_id'])  
    applications = Application.query.filter_by(user_id=user.id).all()
    return render_template('dashboard_seeker.html', applications=applications, user=user)


@job_bp.route('/profile', methods=['GET'])
def profile():
    # Profile page for job seekers that shows user info and application history
    if 'user_id' not in session or session['role'] != 'seeker':
        return redirect('/login')

    user = User.query.get(session['user_id'])
    applications = Application.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, applications=applications)

@job_bp.route('/upload-resume', methods=['POST'])
def upload_resume():
    # Route to handle resume upload/update for job seekers
    if 'user_id' not in session or session['role'] != 'seeker':
        return redirect('/login')
    resume = request.files.get('resume')
    if resume and allowed_file(resume.filename):
        filename = secure_filename(resume.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        resume.save(path)
        # Update the user's resume_path field in the database
        user = User.query.get(session['user_id'])
        user.resume_path = path
        db.session.commit()
        flash("Resume uploaded successfully!")
    else:
        flash("Invalid file or no file selected.")
    return redirect('/profile')

@job_bp.route('/update-experience', methods=['POST'])
def update_experience():
    # Route to update the experience details for a job seeker in their profile
    if 'user_id' not in session or session['role'] != 'seeker':
         return redirect('/login')
    experience = request.form.get('experience')
    user = User.query.get(session['user_id'])
    user.experience = experience
    db.session.commit()
    flash("Experience updated.")
    return redirect('/profile')

@job_bp.route('/view-applicants/<int:job_id>')
def view_applicants(job_id):
    # Employer view of applicants for a specific job
    if 'user_id' not in session or session['role'] != 'employer':
        return redirect('/login')

    job = Job.query.get_or_404(job_id)
    applicants = Application.query.filter_by(job_id=job.id).all()
    return render_template('view_applicants.html', job=job, applicants=applicants)

@job_bp.route('/update-status/<int:app_id>', methods=['POST'])
def update_status(app_id):
    # Employer can update the status of a particular application
    if 'user_id' not in session or session['role'] != 'employer':
        return redirect('/login')
    new_status = request.form.get('status')
    application = Application.query.get_or_404(app_id)
    application.status = new_status
    db.session.commit()
    flash("Application status updated.")
    return redirect(url_for('job.view_applicants', job_id=application.job_id))

@job_bp.route('/close-job/<int:job_id>', methods=['POST'])
def close_job(job_id):
    # Employer can mark a job as closed (no longer accepting applications)
    if 'user_id' not in session or session['role'] != 'employer':
        return redirect('/login')
    job = Job.query.get_or_404(job_id)
    if job.posted_by == session['user_id']:
        job.is_closed = True
        db.session.commit()
        flash("Job marked as closed.")
    return redirect('/dashboard/employer')
