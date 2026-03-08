from flask import Flask, redirect, render_template, request
from models import db,User, StudentProfile,CompanyProfile
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
            approved=False
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
@app.route("/admin/dashboard")
def admin_dashboard():
    companies = User.query.filter_by(role="company", is_approved=False).all()
    return render_template("admin_dashboard.html", companies=companies)


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


@app.route("/")
def home():
    return "Placement Portal Running"

if __name__ == '__main__':
    app.run(debug=True)
# run the Flask application in debug mode, which provides detailed error messages and auto-reloads the server on code changes