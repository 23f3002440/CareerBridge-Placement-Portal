# CareerBridge-Placement-Portal
A full-stack Placement Portal developed with Flask, Jinja2, and SQLite implementing role-based authentication and campus recruitment workflow management.


**MAD-1 Project May 2026**  
23f3002440 / CareerBridge- Placement Portal

---

<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLAlchemy-FFCA28?style=for-the-badge&logo=sqlalchemy&logoColor=white"/>
<img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white"/>

</div>

---
## 📖 Overview

**CareerBridge** is a web-based Placement Portal Application that streamlines the campus recruitment process.
It enables seamless interaction between **Admin (Institute), Companies, and Students** through role-based access.
Admins manage users, placement drives, and system data efficiently.
Companies can post job openings, shortlist candidates, and update recruitment status.
Students can create profiles, apply for jobs, and track their application progress in real time.

---
## 🌟 Benefits:

-Efficient recruitment management<br>
-Faster communication<br>
-Centralized data handling<br>
-Improved placement coordination<br>

---

## 🛠️ Tech Stack

- 🐍 **Python** (Backend)
- ⚗️ **Flask** (Web Framework)
- 💾 **SQLite** (Database)
- 🛢️ **SQLAlchemy** (ORM)
- 🧩 **HTML** & 🎨 **CSS** (Frontend)
- 🅱️ **Bootstrap** (Responsive Design)
  

---
## 📂 Project Structure

```
CareerBridge-Placement-Portal
│
├── static
│   ├── style.css
│   └── images
│
├── templates
│   ├── admin_applications.html
│   ├── admin_companies.html
│   ├── admin_dashboard.html
│   ├── admin_students.html
│   ├── base.html
│   ├── company_dashboard.html
│   ├── create_job.html
│   ├── index.html
│   ├── job_applications.html
│   ├── job_browse.html
│   ├── job_details.html
│   ├── login.html
│   ├── my_applications.html
│   ├── notifications.html
│   ├── register_company.html
│   ├── register_student.html
│   ├── student_dashboard.html
│   └── student_profile.html
│
├── app.py
├── config.py
├── create_admin.py
├── models.py
├── reset_db.py
├── test_admin.py
├── requirements.txt
├── api.yaml
├── README.md
├── .gitignore
└── MODERN APPLICATION DEVELOPMENT 1.pdf
└── instance
    └── database.sqlite    # SQLite database file

```
---
## 🖥️ Live Demo

You can see the video report 📹 at: <br>
👉 https://drive.google.com/file/d/1EEa2k_VXElF8WaEQ03zhklTGXlcXfJ-Q/view?usp=sharing

You can see the project report 📋 at:  
👉 https://drive.google.com/file/d/1h2OE5ty6Xd2UgRzsw8shJpWHpBZIs-l9/view?usp=sharing


---

## ⚙️ Setup from Scratch

### Step 1: Install Python
Make sure Python 3.8+ is installed.
```
python --version
```

### Step 2: Create a virtual environment (recommended)
```bash
cd placement_portal
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the app
```bash
python app.py
```

The app will:
- Auto-create the `placement.db` SQLite database
- Seed the admin user automatically
- Start at: **http://127.0.0.1:5000**

---

## 🔐 Default Login Credentials

| Role  | Username / Email     | Password   |
|-------|----------------------|------------|
| Admin | `admin`              | `admin123` |

---

## 🚀 How to Use (Demo Flow)

### 1. Admin Setup
1. Go to http://127.0.0.1:5000/login
2. Select role = **Admin**, username = `admin`, password = `admin123`
3. You land on the admin dashboard

### 2. Register a Company
1. Open an incognito tab, go to /register/company
2. Fill in details and submit
3. Back in admin → **Companies** → Approve the company

### 3. Company Posts a Drive
1. Login as the company
2. Click **Post New Drive**, fill details, submit
3. Back in admin → **Drives** → Approve the drive

### 4. Student Registers and Applies
1. Go to /register/student
2. Login as student
3. Dashboard shows available drives → click **Apply**
4. Track status in real-time

### 5. Company Shortlists
1. Login as company → View Applications
2. Change status to Shortlisted / Selected / Rejected via dropdown

---


## ✨ Roles & Functionalities

### 🧑‍💼 Admin Dashboard

* Admin is the pre-existing superuser of the application.
* Can approve or reject company registrations.
* Can approve or reject placement drives created by the company.
* Can view and manage all students, companies, and placement drives.
  - Can edit, delete or blacklist students and comapnies if required.
* Can search students or companies by name or ID.

### 🧑‍💼 Company
* Can regsiter and create a company profile.
* Can log in only after admin approval.
* Can create placement drives.
* Can view students applicationss for their drives.
* Can shorlist students and update application status.

### 🧑 Students
* Can resiter, log in, and update their profile.
* Can view approved placement drives.
* Can apply for placement drives.
* Can view application status and placement history. 

---

### Key Terminologies

- 🧑‍💼 **Admin**  
  A user with highest level of access who manages companies, sudents, and placement activities.

- 🧑 **Student**  
  A user who applies for placement drives and participates in recruitment activities.
  
- 👤 **Company**  
 An organization registered in the system that conducts placement drives and recruits students.

- 📅 **Placement Drive**  
  A recruitment drive created by a company.
  - Attributes:
    * Drive ID
    * Comapny ID
    * Job Title
    * Job Description
    * Eligibility Criteria
    * Application Deadline
    * Status (Pending/Approved/Closed)
    * Extra Fields

- 📝 **Application**  
  A record of a student applying to a palcement drive.
  - Attributes:
    * Application ID
    * Student ID
    * Drive ID
    * Application Date
    * Status (Applied / Shortlisted / Selected / Rejected)
    * Extra fields

- 📝 **Company Profile**  
  Details of a registered company.
  - Attributes:
    * Company ID
    * Company Name
    * HR Contact
    * Website
    * Approval Status
    * Extra fields
---

<img width="1024" height="1536" alt="ChatGPT Image Mar 3, 2026, 11_26_15 AM" src="https://github.com/user-attachments/assets/df7d6a5b-e8da-4d4f-ada1-f8bb35a7d6d8" />


BY : @23F3002440<BR>
     MANSI KUMARI
