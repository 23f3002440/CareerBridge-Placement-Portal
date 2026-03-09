from flask import Flask, redirect, render_template, request, session
from functools import wraps
from models import db,User, StudentProfile,CompanyProfile,JobPosition,Application,Placement,Notification
# we have created database in models.py hence importing database from it
from sqlalchemy import and_
import os

app = Flask(__name__)
#create main Flask app object
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'placement.db')}"
# database is created 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# disables the feature that tracks every object change
# saves memory
app.secret_key = 'your_secret_key_here'  # Change this to a secure key in production
db.init_app(app)

# Ensure instance folder exists
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

# DECORATOR FOR COMPANY ROUTES
def company_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'].get('role') != 'company':
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# DECORATOR FOR STUDENT ROUTES
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'].get('role') != 'student':
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# DECORATOR FOR ADMIN ROUTES
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'].get('role') != 'admin':
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
# app interact  with the database using the app context
with app.app_context():
    db.create_all()
# create all the tables that are defined in models.py
    # Check if admin exists
    admin = User.query.filter_by(name="admin").first()
    if not admin:
        admin = User(
            name="admin", 
            email="admin@example.com",
            password="admin123",
            role="admin",
            is_approved=True,
            is_active=True
        )
        # add the admin user to the database
        
        db.session.add(admin)
        db.session.commit()
        
# STUDENT REGISTRATION
@app.route("/register/student", methods=["GET","POST"])
def register_student():
    error = None
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        email = request.form.get("email", "").strip()
        
        # Validation
        if not name or not password:
            error = "Username and password are required"
        elif len(password) < 4:
            error = "Password must be at least 4 characters long"
        elif not email:
            error = "Email is required"
        else:
            # Check if user already exists
            existing_user = User.query.filter_by(name=name).first()
            if existing_user:
                error = "Username already exists. Please choose a different username."
            else:
                existing_email = User.query.filter_by(email=email).first()
                if existing_email:
                    error = "Email already registered. Please use a different email."
                else:
                    try:
                        student = User(
                            name=name,
                            email=email,
                            password=password,
                            role="student",
                            is_approved=True,  # students approved immediately
                            is_active=True
                        )

                        db.session.add(student)
                        db.session.commit()
                        return redirect("/login")
                    except Exception as e:
                        db.session.rollback()
                        error = f"Registration failed: {str(e)}"

    return render_template("register_student.html", error=error)


# COMPANY REGISTRATION
@app.route("/register/company", methods=["GET","POST"])
def register_company():
    error = None
    success = None
    
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        email = request.form.get("email", "").strip()
        
        # Validation
        if not name or not password:
            error = "Company name and password are required"
        elif len(password) < 4:
            error = "Password must be at least 4 characters long"
        elif not email:
            error = "Email is required"
        else:
            # Check if user already exists
            existing_user = User.query.filter_by(name=name).first()
            if existing_user:
                error = "Company name already exists. Please choose a different name."
            else:
                existing_email = User.query.filter_by(email=email).first()
                if existing_email:
                    error = "Email already registered. Please use a different email."
                else:
                    try:
                        company = User(
                            name=name,
                            email=email,
                            password=password,
                            role="company",
                            is_approved=False,
                            is_active=True
                        )

                        db.session.add(company)
                        db.session.commit()
                        success = "Registration successful! Waiting for admin approval. Please login after approval."
                    except Exception as e:
                        db.session.rollback()
                        error = f"Registration failed: {str(e)}"

    return render_template("register_company.html", error=error, success=success)


# LOGIN SYSTEM
@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        name = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not password:
            error = "Username and password are required"
        else:
            user = User.query.filter(and_(User.name==name, User.password==password)).first()
            
            if user:
                if not user.is_active:
                    error = "Your account has been deactivated. Please contact support."
                elif user.role == "company" and not user.is_approved:
                    error = "Your company account is pending admin approval. Please wait."
                else:
                    session['user'] = {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'role': user.role
                    }
                    
                    if user.role == "admin":
                        return redirect("/admin/dashboard")
                    elif user.role == "student":
                        return redirect("/student/dashboard")
                    elif user.role == "company":
                        return redirect("/company/dashboard")
            else:
                error = "Invalid username or password"

    return render_template("login.html", error=error)


# ROLE BASED DASHBOARDS
# ADMIN DASHBOARD
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    total_companies = User.query.filter_by(role="company").count()
    pending_companies = User.query.filter_by(role="company", is_approved=False).count()
    total_students = User.query.filter_by(role="student").count()
    total_jobs = JobPosition.query.count()
    pending_jobs = JobPosition.query.filter_by(is_approved=False).count()
    total_applications = Application.query.count()
    
    companies = User.query.filter_by(role="company").all()
    students = User.query.filter_by(role="student").all()
    jobs = JobPosition.query.all()
    
    return render_template("admin_dashboard.html",
                           total_companies=total_companies,
                           pending_companies=pending_companies,
                           total_students=total_students,
                           total_jobs=total_jobs,
                           pending_jobs=pending_jobs,
                           total_applications=total_applications,
                           companies=companies,
                           students=students,
                           jobs=jobs)


@app.route("/company/dashboard")
@company_required
def company_dashboard():
    # Verify company is approved
    user = User.query.get(session["user"]["id"])
    if not user.is_approved:
        return render_template("company_dashboard.html", approved=False, company=None)
    
    # Get company profile
    company_profile = CompanyProfile.query.filter_by(user_id=user.id).first()
    if not company_profile:
        # Create company profile if it doesn't exist
        company_profile = CompanyProfile(user_id=user.id, company_name=user.name, industry="")
        db.session.add(company_profile)
        db.session.commit()
    
    # Get all jobs for this company
    jobs = JobPosition.query.filter_by(company_id=company_profile.id).all()
    
    # Calculate statistics
    total_jobs = len(jobs)
    active_jobs = len([j for j in jobs if j.is_active])
    
    # Get all applications
    all_applications = []
    for job in jobs:
        all_applications.extend(job.applications)
    
    total_applications = len(all_applications)
    shortlisted = len([a for a in all_applications if a.status == "Shortlisted"])
    selected = len([a for a in all_applications if a.status == "Selected"])
    rejected = len([a for a in all_applications if a.status == "Rejected"])
    
    return render_template("company_dashboard.html",
                          approved=True,
                          company=company_profile,
                          jobs=jobs,
                          total_jobs=total_jobs,
                          active_jobs=active_jobs,
                          total_applications=total_applications,
                          shortlisted=shortlisted,
                          selected=selected,
                          rejected=rejected)

# COMPANY MANAGEMENT
@app.route("/admin/company/approve/<int:user_id>")
@admin_required
def approve_company(user_id):
    company = User.query.get(user_id)
    if company:
        company.is_approved = True
        db.session.commit()
    return redirect("/admin/dashboard")

@app.route("/admin/company/reject/<int:user_id>")
@admin_required
def reject_company(user_id):
    company = User.query.get(user_id)
    if company:
        db.session.delete(company)
        db.session.commit()
    return redirect("/admin/dashboard")


# JOB MANAGEMENT
@app.route("/admin/job/approve/<int:job_id>")
@admin_required
def approve_job(job_id):
    job = JobPosition.query.get(job_id)
    if job:
        job.is_approved = True
        db.session.commit()
    return redirect("/admin/dashboard")

@app.route("/admin/job/reject/<int:job_id>")
@admin_required
def reject_job(job_id):
    job = JobPosition.query.get(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
    return redirect("/admin/dashboard")


# SEARCH STUDENTS
@app.route("/admin/students")
@admin_required
def search_students():
    query = request.args.get("query")
    students = User.query.filter(User.role=="student").join(StudentProfile)
    if query:
        students = students.filter((User.name.contains(query)) | 
                                   (StudentProfile.roll_no.contains(query)) |
                                   (User.email.contains(query)))
    students = students.all()
    return render_template("admin_students.html", students=students)


# SEARCH COMPANIES
@app.route("/admin/companies")
@admin_required
def search_companies():
    query = request.args.get("query")
    companies = User.query.filter(User.role=="company").join(CompanyProfile)
    if query:
        companies = companies.filter((User.name.contains(query)) |
                                     (CompanyProfile.industry.contains(query)) |
                                     (User.email.contains(query)))
    companies = companies.all()
    return render_template("admin_companies.html", companies=companies)


# VIEW ALL APPLICATIONS
@app.route("/admin/applications")
@admin_required
def admin_view_applications():
    applications = Application.query.all()
    return render_template("admin_applications.html", applications=applications)


# REACTIVATE USER (student or company)
@app.route("/admin/user/reactivate/<int:user_id>")
@admin_required
def reactivate_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_active = True  # Set active back to True
        db.session.commit()
        return redirect("/admin/dashboard")  # Redirect to admin dashboard
    return "User not found"

# DEACTIVATE USER (student or company)
@app.route("/admin/user/deactivate/<int:user_id>")
@admin_required
def deactivate_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_active = False  # Set active to False
        db.session.commit()
        return redirect("/admin/dashboard")  # Redirect to admin dashboard
    return "User not found"


# Create Job
@app.route("/company/job/new", methods=["GET", "POST"])
@company_required
def create_job():
    # Verify company is approved
    user = User.query.get(session["user"]["id"])
    if not user.is_approved:
        return "Your company is not approved yet. Please wait for admin approval."
    
    if request.method == "POST":
        # Get company profile
        company_profile = CompanyProfile.query.filter_by(user_id=user.id).first()
        if not company_profile:
            return "Company profile not found"
        
        job = JobPosition(
            company_id=company_profile.id,
            title=request.form["title"],
            description=request.form.get("description", ""),
            skills=request.form.get("skills", ""),
            experience=request.form.get("experience", ""),
            salary=request.form.get("salary", 0, type=int),
            salary_max=request.form.get("salary_max", 0, type=int),
            location=request.form.get("location", ""),
            is_active=True,
            is_approved=False  # Requires admin approval
        )
        db.session.add(job)
        db.session.commit()
        return redirect("/company/dashboard")
    return render_template("create_job.html")

# Close Job
@app.route("/company/job/close/<int:job_id>")
@company_required
def close_job(job_id):
    job = JobPosition.query.get(job_id)
    company_profile = CompanyProfile.query.filter_by(user_id=session["user"]["id"]).first()
    if job and company_profile and job.company_id == company_profile.id:
        job.is_active = False
        db.session.commit()
    return redirect("/company/dashboard")

# View Applications
@app.route("/company/job/applications/<int:job_id>")
@company_required
def view_applications(job_id):
    job = JobPosition.query.get(job_id)
    company_profile = CompanyProfile.query.filter_by(user_id=session["user"]["id"]).first()
    if job and company_profile and job.company_id == company_profile.id:
        applications = Application.query.filter_by(job_id=job_id).all()
        return render_template("job_applications.html", applications=applications, job=job)
    return "Unauthorized"

# Shortlist Application
@app.route("/company/application/shortlist/<int:app_id>")
@company_required
def shortlist_application(app_id):
    app_obj = Application.query.get(app_id)
    company_profile = CompanyProfile.query.filter_by(user_id=session["user"]["id"]).first()
    if app_obj and company_profile and app_obj.job.company_id == company_profile.id:
        app_obj.status = "Shortlisted"
        db.session.commit()
    return redirect(f"/company/job/applications/{app_obj.job_id}")

# Select Application (Accept/Offer)
@app.route("/company/application/select/<int:app_id>")
@company_required
def select_application(app_id):
    app_obj = Application.query.get(app_id)
    company_profile = CompanyProfile.query.filter_by(user_id=session["user"]["id"]).first()
    if app_obj and company_profile and app_obj.job.company_id == company_profile.id:
        app_obj.status = "Selected"
        db.session.commit()
    return redirect(f"/company/job/applications/{app_obj.job_id}")

# Reject Application
@app.route("/company/application/reject/<int:app_id>")
@company_required
def reject_application(app_id):
    app_obj = Application.query.get(app_id)
    company_profile = CompanyProfile.query.filter_by(user_id=session["user"]["id"]).first()
    if app_obj and company_profile and app_obj.job.company_id == company_profile.id:
        app_obj.status = "Rejected"
        db.session.commit()
    return redirect(f"/company/job/applications/{app_obj.job_id}")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# HOME ROUTE
@app.route("/")
def home():
    return render_template("index.html")


# ================== STUDENT ROUTES ==================

# STUDENT DASHBOARD
@app.route("/student/dashboard")
@student_required
def student_dashboard():
    user = User.query.get(session["user"]["id"])
    student_profile = StudentProfile.query.filter_by(user_id=user.id).first()
    
    if not student_profile:
        return redirect("/student/profile/edit")
    
    # Get statistics
    total_applications = Application.query.filter_by(student_id=student_profile.id).count()
    applied = len([a for a in student_profile.applications if a.status == "Applied"])
    shortlisted = len([a for a in student_profile.applications if a.status == "Shortlisted"])
    selected = len([a for a in student_profile.applications if a.status == "Selected"])
    rejected = len([a for a in student_profile.applications if a.status == "Rejected"])
    
    # Get recent applications
    recent_applications = Application.query.filter_by(student_id=student_profile.id).order_by(
        Application.applied_at.desc()
    ).limit(5).all()
    
    # Get notifications
    unread_notifications = Notification.query.filter_by(
        student_id=student_profile.id, is_read=False
    ).order_by(Notification.created_at.desc()).all()
    
    return render_template("student_dashboard.html",
                          student=student_profile,
                          total_applications=total_applications,
                          applied=applied,
                          shortlisted=shortlisted,
                          selected=selected,
                          rejected=rejected,
                          recent_applications=recent_applications,
                          unread_notifications=unread_notifications)


# VIEW & EDIT STUDENT PROFILE
@app.route("/student/profile/edit", methods=["GET", "POST"])
@student_required
def edit_student_profile():
    user = User.query.get(session["user"]["id"])
    student_profile = StudentProfile.query.filter_by(user_id=user.id).first()
    
    if request.method == "POST":
        if not student_profile:
            student_profile = StudentProfile(user_id=user.id, password=user.password)
        
        student_profile.roll_no = request.form.get("roll_no", "")
        student_profile.course = request.form.get("course", "")
        student_profile.cgpa = float(request.form.get("cgpa", 0))
        student_profile.graduation_year = int(request.form.get("graduation_year", 0))
        student_profile.skills = request.form.get("skills", "")
        student_profile.phone = request.form.get("phone", "")
        student_profile.address = request.form.get("address", "")
        student_profile.bio = request.form.get("bio", "")
        student_profile.github = request.form.get("github", "")
        student_profile.linkedin = request.form.get("linkedin", "")
        student_profile.resume_link = request.form.get("resume_link", "")
        
        if not student_profile.id:
            db.session.add(student_profile)
        db.session.commit()
        
        return redirect("/student/dashboard")
    
    return render_template("student_profile.html", student=student_profile, user=user)


# BROWSE & SEARCH JOBS
@app.route("/student/jobs")
@student_required
def browse_jobs():
    user = User.query.get(session["user"]["id"])
    student_profile = StudentProfile.query.filter_by(user_id=user.id).first()
    
    # Get search parameters
    search_query = request.args.get("search", "").strip()
    filter_by = request.args.get("filter", "all")  # all, company, position, skills
    
    # Get all approved jobs that are active
    jobs = JobPosition.query.filter_by(is_approved=True, is_active=True).all()
    
    # Apply filters
    if search_query:
        if filter_by == "company":
            jobs = [j for j in jobs if search_query.lower() in j.company.company_name.lower()]
        elif filter_by == "position":
            jobs = [j for j in jobs if search_query.lower() in j.title.lower()]
        elif filter_by == "skills":
            jobs = [j for j in jobs if search_query.lower() in j.skills.lower()]
        else:  # all
            jobs = [j for j in jobs if (search_query.lower() in j.title.lower() or 
                                       search_query.lower() in j.company.company_name.lower() or
                                       search_query.lower() in j.skills.lower())]
    
    # Get student's applied jobs
    applied_job_ids = [app.job_id for app in student_profile.applications] if student_profile else []
    
    return render_template("job_browse.html",
                          jobs=jobs,
                          applied_job_ids=applied_job_ids,
                          search_query=search_query,
                          filter_by=filter_by)


# VIEW JOB DETAILS & APPLY
@app.route("/student/job/<int:job_id>")
@student_required
def view_job_details(job_id):
    user = User.query.get(session["user"]["id"])
    student_profile = StudentProfile.query.filter_by(user_id=user.id).first()
    job = JobPosition.query.get(job_id)
    
    if not job or not job.is_approved or not job.is_active:
        return "Job not found or not available"
    
    # Check if already applied
    application = Application.query.filter_by(
        student_id=student_profile.id,
        job_id=job_id
    ).first()
    
    return render_template("job_details.html",
                          job=job,
                          student=student_profile,
                          application=application)


# APPLY FOR JOB
@app.route("/student/job/<int:job_id>/apply", methods=["POST"])
@student_required
def apply_job(job_id):
    user = User.query.get(session["user"]["id"])
    student_profile = StudentProfile.query.filter_by(user_id=user.id).first()
    job = JobPosition.query.get(job_id)
    
    if not job:
        return "Job not found"
    
    # Check if already applied
    existing_application = Application.query.filter_by(
        student_id=student_profile.id,
        job_id=job_id
    ).first()
    
    if existing_application:
        return redirect(f"/student/job/{job_id}")
    
    # Create application
    application = Application(
        student_id=student_profile.id,
        job_id=job_id,
        status="Applied"
    )
    
    db.session.add(application)
    
    # Create notification
    notification = Notification(
        student_id=student_profile.id,
        job_id=job_id,
        title=f"Application Submitted",
        message=f"Your application for {job.title} at {job.company.company_name} has been submitted.",
        notification_type="applied"
    )
    
    db.session.add(notification)
    db.session.commit()
    
    return redirect(f"/student/job/{job_id}")


# VIEW MY APPLICATIONS
@app.route("/student/applications")
@student_required
def my_applications():
    user = User.query.get(session["user"]["id"])
    student_profile = StudentProfile.query.filter_by(user_id=user.id).first()
    
    if not student_profile:
        return redirect("/student/profile/edit")
    
    # Get applications sorted by applied date
    applications = Application.query.filter_by(
        student_id=student_profile.id
    ).order_by(Application.applied_at.desc()).all()
    
    # Group by status
    status_groups = {
        "Applied": [a for a in applications if a.status == "Applied"],
        "Shortlisted": [a for a in applications if a.status == "Shortlisted"],
        "Selected": [a for a in applications if a.status == "Selected"],
        "Rejected": [a for a in applications if a.status == "Rejected"]
    }
    
    return render_template("my_applications.html",
                          applications=applications,
                          status_groups=status_groups)


# VIEW NOTIFICATIONS
@app.route("/student/notifications")
@student_required
def view_notifications():
    user = User.query.get(session["user"]["id"])
    student_profile = StudentProfile.query.filter_by(user_id=user.id).first()
    
    if not student_profile:
        return redirect("/student/profile/edit")
    
    notifications = Notification.query.filter_by(
        student_id=student_profile.id
    ).order_by(Notification.created_at.desc()).all()
    
    return render_template("notifications.html", notifications=notifications)


# MARK NOTIFICATION AS READ
@app.route("/student/notification/<int:notif_id>/read")
@student_required
def mark_notification_read(notif_id):
    notification = Notification.query.get(notif_id)
    if notification:
        notification.is_read = True
        db.session.commit()
    
    return redirect("/student/notifications")


if __name__ == '__main__':
    app.run(debug=True)
# run the Flask application in debug mode, which provides detailed error messages and auto-reloads the server on code changes