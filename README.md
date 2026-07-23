# Gym Management System

A modern **Gym Management System** built with **Python, Django, Bootstrap, HTML, CSS, JavaScript, and SQLite**. The system helps gym administrators efficiently manage members, 
trainers, membership plans, payments, attendance, equipment, workout plans, enquiries, and feedback through a clean dashboard interface.

## Project Overview

This project is designed to automate daily gym operations and reduce manual paperwork. It provides separate dashboards for administrators and members with role-based authentication.

The system allows administrators to manage every aspect of the gym while members can access their personal information, workout plans, attendance, payments, memberships, and submit feedback.

# Features

## Admin Panel

### Dashboard
- Admin Dashboard
- Statistics Cards
- Quick Navigation
- Responsive UI

### Member Management
- Add Member
- Edit Member
- Delete Member
- Search Members
- Assign Membership Plan
- Assign Trainer

### Membership Plans
- Add Plan
- Edit Plan
- Delete Plan
- Plan Description
- Duration Management

### Trainer Management
- Add Trainer
- Edit Trainer
- Delete Trainer
- Specialization
- Shift Timing
- Experience Management

### Payment Management
- Record Payments
- Payment Status
- Payment Mode
- Payment Notes
- Member-wise Filter
- Status Filter
- Membership Auto Update

### Attendance Management
- Mark Attendance
- Date-wise Filter
- Member-wise Filter
- Attendance History

### Equipment Management
- Add Equipment
- Edit Equipment
- Delete Equipment
- Purchase Date
- Equipment Price
- Units Tracking

### Workout & Diet Plans
- Assign Workout Plan
- Assign Diet Plan
- Edit Workout Plan
- Delete Workout Plan
- Member-wise Filtering

### Enquiry Management
- View Contact Enquiries
- Update Status
- Track New / Seen / Resolved

### Feedback Management
- View Member Feedback
- Filter by Member

# Member Panel

Members have their own dashboard where they can:

- View Dashboard Statistics
- View Profile
- Edit Profile
- Change Password
- View Membership Details
- View Payment History
- View Attendance History
- View Workout & Diet Plans
- Submit Feedback
- View Previous Feedback

---

# Authentication

- Custom User Model
- Role-Based Login
- Admin Login
- Member Login
- Session Authentication

Roles:
- ADMIN
- MEMBER


# Technologies Used

### Backend

- Python
- Django

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Bootstrap Icons

### Database

- SQLite3

### Version Control

- Git
- GitHub

# Modules

- User Authentication
- Dashboard
- Member Management
- Trainer Management
- Membership Plans
- Payments
- Attendance
- Equipment
- Workout Plans
- Diet Plans
- Feedback
- Enquiries

# Installation

Clone the repository

Move into the project directory

cd GumProject


Create Virtual Environment

python -m venv env

Activate Environment

### in Windows

venv\Scripts\activate

### macOS / Linux

source venv/bin/activate


Install Dependencies

pip install -r requirements.txt

Apply Migrations

python manage.py migrate

Create Superuser

python manage.py createsuperuser

Run Server

python manage.py runserver

Open
http://127.0.0.1:8000/


# UI Features

- Responsive Design
- Modern Dashboard
- Gradient Headers
- Section-Based Layout
- Interactive Tables
- Card Components
- Bootstrap Icons
- Mobile Friendly
- Clean Typography



GitHub: https://github.com/aaryan07thakur

This project is developed for educational and portfolio purposes.

Feel free to use, modify, and improve it.
