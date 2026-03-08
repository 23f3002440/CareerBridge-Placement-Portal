from flask import Flask, redirect, render_template, request, session
from functools import wraps
from models import db,User, StudentProfile,CompanyProfile,JobPosition,Application,Placement
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
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        email = request.form.get("email", f"{name}@student.example.com")

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

    return render_template("register_student.html")


# COMPANY REGISTRATION
@app.route("/register/company", methods=["GET","POST"])
def register_company():

    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        email = request.form.get("email", f"{name}@company.example.com")

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

        return "Waiting for admin approval. Please login after approval."

    return render_template("register_company.html")


# LOGIN SYSTEM
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]

        user = User.query.filter(and_(User.name==name, User.password==password)).first()
        
        if user:
            if not user.is_active:
                return "User account has been deactivated"
            
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
                if user.is_approved:
                    return redirect("/company/dashboard")
                else:
                    return "Company waiting for admin approval"

        return "Invalid login"

    return render_template("login.html")


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


@app.route("/student/dashboard")
@student_required
def student_dashboard():
    return render_template("student_dashboard.html")


@app.route("/company/dashboard")
@company_required
def company_dashboard():
    jobs = JobPosition.query.filter_by(company_id=session["user"]["id"]).all()
    return render_template("company_dashboard.html", jobs=jobs)

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
def view_applications():
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
    if request.method == "POST":
        job = JobPosition(
            company_id=session["user"]["id"],
            title=request.form["title"],
            description=request.form.get("description", ""),
            salary=request.form.get("salary", 0),
            location=request.form.get("location", ""),
            is_active=True,
            is_approved=False  # optional admin approval
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
    if job and job.company_id == session["user"]["id"]:
        job.is_active = False
        db.session.commit()
    return redirect("/company/dashboard")

# View Applications
@app.route("/company/job/applications/<int:job_id>")
@company_required
def view_applications(job_id):
    job = JobPosition.query.get(job_id)
    if job and job.company_id == session["user"]["id"]:
        applications = Application.query.filter_by(job_id=job_id).all()
        return render_template("job_applications.html", applications=applications, job=job)
    return "Unauthorized"

# Shortlist / Reject
@app.route("/company/application/shortlist/<int:app_id>")
@company_required
def shortlist_application(app_id):
    app_obj = Application.query.get(app_id)
    if app_obj and app_obj.job.company_id == session["user"]["id"]:
        app_obj.status = "Shortlisted"
        db.session.commit()
    return redirect(f"/company/job/applications/{app_obj.job_id}")

@app.route("/company/application/reject/<int:app_id>")
@company_required
def reject_application(app_id):
    app_obj = Application.query.get(app_id)
    if app_obj and app_obj.job.company_id == session["user"]["id"]:
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

if __name__ == '__main__':
    app.run(debug=True)
# run the Flask application in debug mode, which provides detailed error messages and auto-reloads the server on code changes