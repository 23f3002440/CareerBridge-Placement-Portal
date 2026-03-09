from flask_sqlalchemy import SQLAlchemy
# package - flask_sqlalchemy
# class - SQLAlchemy
db = SQLAlchemy()
# create database instance named db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, student, company
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)  # For company approval

    # One-to-one relationships
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, lazy='select')
    company_profile = db.relationship('CompanyProfile', backref='user', uselist=False, lazy='select')
class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    resume_link = db.Column(db.String(200), nullable=True)
    graduation_year = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.String(500), nullable=True)  # Comma-separated skills
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    github = db.Column(db.String(200), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    profile_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    applications = db.relationship('Application', backref='student', lazy=True)
    notifications = db.relationship('Notification', backref='student', lazy=True)
    # creating connection one to one relationship between user and student
class CompanyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    industry = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)

    jobs = db.relationship('JobPosition', backref='company', lazy=True)
    # creating connection one to one relationship between user and company
    
class JobPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    skills = db.Column(db.String(500))  # Required skills
    experience = db.Column(db.String(100))  # Experience required
    salary = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)  # Salary range upper limit
    location = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)  # Active/Closed status
    is_approved = db.Column(db.Boolean, default=False)  # Admin approval for job postings
    created_at = db.Column(db.DateTime, default=db.func.now())
    company_id = db.Column(db.Integer, db.ForeignKey('company_profile.id'), nullable=False)

    applications = db.relationship('Application', backref='job', lazy=True)
    
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_position.id'), nullable=False)
    status = db.Column(db.String(50), default="Applied")  # Applied, Shortlisted, Selected, Rejected
    applied_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    placement = db.relationship('Placement', backref='application', uselist=False)

class Placement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    joining_date = db.Column(db.String(50))
    package = db.Column(db.Integer)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_position.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # applied, shortlisted, selected, rejected
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    job = db.relationship('JobPosition', backref='notifications')

    