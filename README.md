
# 🚀 Flask Job Portal Project

A fully functional Job Portal web application built using Flask 
Includes user authentication, job posting, application management, and user dashboards.



## ✨ Features

- 👤 **User Registration and Login** (Employer & Job Seeker)
- 📝 **Employers can post jobs**
- 📄 **Job Seekers can apply to jobs with a cover letter and resume (PDF)**
- 📋 **All users can view job listings**
- 📂 **Resume upload system (PDF only)**
- 🧑‍💼 **Employer Dashboard**
  - View posted jobs
  - View applicants for each job
- 👩‍💻 **Seeker Dashboard**
  - View applied jobs
  - Track application status
- ✅ Flash messages for feedback
- 🔐 Role-based access and session management
- 📧 Optional email notifications via SMTP
- 🎨 Clean UI with custom CSS



## ⚙️ How to Run

1. **Clone the repo or unzip the folder**
2. **Install Python packages**  
   Run in terminal:

   pip install flask flask_sqlalchemy werkzeug python-dotenv

3. **Start the Flask app**

   python app.py

4. Open your browser and go to:  
   `http://127.0.0.1:5000/`



## 👥 User Roles

### Employer
- ✅ Post jobs via `/post-job`
- ✅ View posted jobs and applicants

### Job Seeker
- ✅ Browse job listings (`/jobs`)
- ✅ Apply with resume via `/apply/<job_id>`
- ✅ View application history via dashboard



## 🧩 Project Modules

- `/post-job` – Job posting form
- `/jobs` – Public job listings
- `/apply/<job_id>` – Job application with file upload
- `/dashboard/employer` – Dashboard for employers
- `/dashboard/seeker` – Dashboard for seekers
- Authentication and session management with `auth.py`
- Flash messages and user feedback

---

## 📁 Folder Structure

job_project/
│
├── app.py
├── auth.py
├── jobs.py
├── dashboard_employer.py
├── dashboard_seeker.py
├── models.py
├── mail_config.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   
│
├── static/
│   └── style.css
│
└── uploads/
    └── resumes (PDF uploads)




## 📬 Email Notifications (

- Enable Gmail 2FA and create an App Password
- Add credentials to `mail_config.py`
- Automatically notify employers when a job is applied for


## 📝 License

This project is open-source and free to use for educational purposes.
