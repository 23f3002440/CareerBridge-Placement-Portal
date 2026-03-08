from flask import Flask, redirect, render_template, request
from models import db,User, StudentProfile,CompanyProfile,JobPosition,Application,Placement
# we have created database in models.py hence importing database from it
from sqlalchemy import and_
app = Flask(__name__)
#create main Flask app object
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///placement.db"
# database is created 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# disables the feature that tracks every object change
# saves memory
db.init_app(app)
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

        student = User(
            name=name,
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

        company = User(
            name=name,
            password=password,
            role="company",
            is_approved=False,
            is_active=True
        )

        db.session.add(company)
        db.session.commit()

        return "Waiting for admin approval"

    return render_template("register_company.html")
# Test route

# LOGIN SYSTEM

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]

        user = User.query.filter(and_(User.name==name, User.password==password)).first()
        
        if user:
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


# COMPANY MANAGEMENT
@app.route("/admin/company/approve/<int:user_id>")
def approve_company(user_id):
    company = User.query.get(user_id)
    company.is_approved = True
    db.session.commit()
    return redirect("/admin/dashboard")

@app.route("/admin/company/reject/<int:user_id>")
def reject_company(user_id):
    company = User.query.get(user_id)
    db.session.delete(company)
    db.session.commit()
    return redirect("/admin/dashboard")




# JOB MANAGEMENT
from flask import Flask, redirect, render_template, request
from models import db,User, StudentProfile,CompanyProfile,JobPosition,Application,Placement
# we have created database in models.py hence importing database from it
from sqlalchemy import and_
app = Flask(__name__)
#create main Flask app object
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///placement.db"
# database is created 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# disables the feature that tracks every object change
# saves memory
db.init_app(app)
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

        student = User(
            name=name,
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

        company = User(
            name=name,
            password=password,
            role="company",
            is_approved=False,
            is_active=True
        )

        db.session.add(company)
        db.session.commit()

        return "Waiting for admin approval"

    return render_template("register_company.html")
# Test route

# LOGIN System

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]

        user = User.query.filter(and_(User.name==name, User.password==password)).first()
        
        if user:
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


# COMPANY MANAGEMENT
@app.route("/admin/company/approve/<int:user_id>")
def approve_company(user_id):
    company = User.query.get(user_id)
    company.is_approved = True
    db.session.commit()
    return redirect("/admin/dashboard")

@app.route("/admin/company/reject/<int:user_id>")
def reject_company(user_id):
    company = User.query.get(user_id)
    db.session.delete(company)
    db.session.commit()
    return redirect("/admin/dashboard")




# JOB MANAGEMENT
@app.route("/admin/job/approve/<int:job_id>")
def approve_job(job_id):
    job = JobPosition.query.get(job_id)
    if job:
        job.is_approved = True
        db.session.commit()
    return redirect("/admin/dashboard")

@app.route("/admin/job/reject/<int:job_id>")
def reject_job(job_id):
    job = JobPosition.query.get(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
    return redirect("/admin/dashboard")


# BLACKLIST/DEACTIVATED USERS
@app.route("/admin/job/approve/<int:job_id>")
def approve_job(job_id):
    job = JobPosition.query.get(job_id)
    job.is_approved = True
    db.session.commit()
    return redirect("/admin/dashboard")

@app.route("/admin/job/reject/<int:job_id>")
def reject_job(job_id):
    job = JobPosition.query.get(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect("/admin/dashboard")



@app.route("/student/dashboard")
def student_dashboard():
    return render_template("student_dashboard.html")


@app.route("/company/dashboard")
def company_dashboard():
    return render_template("company_dashboard.html")


# ADMIN APPROVAL COMPANIES
@app.route("/approve/<int:user_id>")
def approve_company(user_id):

    company = User.query.get(user_id)
    if company:
        company.is_approved = True
        db.session.commit()
    return redirect("/admin/dashboard")


# SEARCH STUDENTS
@app.route("/admin/students")
def search_students():
    query = request.args.get("query")
    students = User.query.filter(User.role=="student")
    if query:
        students = students.filter((User.name.contains(query)) | 
                                   (StudentProfile.roll_no.contains(query)) |
                                   (User.email.contains(query)))
    students = students.all()
    return render_template("admin_students.html", students=students)


# SEARCH COMPANIES
@app.route("/admin/companies")
def search_companies():
    query = request.args.get("query")
    companies = User.query.filter(User.role=="company")
    if query:
        companies = companies.filter((User.name.contains(query)) |
                                     (CompanyProfile.industry.contains(query)) |
                                     (User.email.contains(query)))
    companies = companies.all()
    return render_template("admin_companies.html", companies=companies)


# REACTIVATE USER (student or company)
@app.route("/reactivate/<int:user_id>")
def reactivate_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_active = True  # Set active back to True
        db.session.commit()
        return redirect("/admin/dashboard")  # Redirect to admin dashboard
    return "User not found"



@app.route("/")
def home():
    return "Placement Portal Running"

if __name__ == '__main__':
    app.run(debug=True)
# run the Flask application in debug mode, which provides detailed error messages and auto-reloads the server on code changes



@app.route("/student/dashboard")
def student_dashboard():
    return render_template("student_dashboard.html")


@app.route("/company/dashboard")
def company_dashboard():
    return render_template("company_dashboard.html")


# ADMIN APPROVAL COMPANIES
@app.route("/approve/<int:user_id>")
def approve_company(user_id):

    company = User.query.get(user_id)
    if company:
        company.is_approved = True
        db.session.commit()
    return redirect("/admin/dashboard")


# SEARCH STUDENTS
@app.route("/admin/students")
def search_students():
    query = request.args.get("query")
    students = User.query.filter(User.role=="student")
    if query:
        students = students.filter((User.name.contains(query)) | 
                                   (StudentProfile.roll_no.contains(query)) |
                                   (User.email.contains(query)))
    students = students.all()
    return render_template("admin_students.html", students=students)


# SEARCH COMPANIES
@app.route("/admin/companies")
def search_companies():
    query = request.args.get("query")
    companies = User.query.filter(User.role=="company")
    if query:
        companies = companies.filter((User.name.contains(query)) |
                                     (CompanyProfile.industry.contains(query)) |
                                     (User.email.contains(query)))
    companies = companies.all()
    return render_template("admin_companies.html", companies=companies)


# REACTIVATE USER (student or company)
@app.route("/reactivate/<int:user_id>")
def reactivate_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_active = True  # Set active back to True
        db.session.commit()
        return redirect("/admin/dashboard")  # Redirect to admin dashboard
    return "User not found"



@app.route("/")
def home():
    return "Placement Portal Running"

if __name__ == '__main__':
    app.run(debug=True)
# run the Flask application in debug mode, which provides detailed error messages and auto-reloads the server on code changes