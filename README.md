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
🔹 Benefits:

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


## 🖥️ Live Demo

You can use the app at:  
👉 [https://vehicle-parking-app-v1-jnm1.onrender.com/](https://vehicle-parking-app-v1-jnm1.onrender.com/)

> ⚠️ **Note:**  
> As the app is deployed on Render's free tier, it may take 10-15 minutes to wake up from sleep mode if there's no recent traffic! Please be patient after clicking the link.

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
