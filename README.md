🏫 YouExcel Management System
A complete web-based training center management system built with Django, designed to manage Admin, Staff/Teachers, and Students efficiently.

🔧 Features
✅ Admin Panel:
Login/Logout functionality

Add/View/Update/Delete Staff & Students

Assign courses and subjects

View feedback and attendance reports

👨‍🏫 Staff/Teacher Dashboard:
Secure login

View assigned subjects and students

Mark daily attendance

Submit feedback and leave requests

👨‍🎓 Student Dashboard:
Secure login

View personal profile

View attendance records

Submit feedback

💻 Tech Stack
Backend: Django (Python)

Frontend: HTML, CSS, Bootstrap

Database: SQLite (default) or MySQL (optional)

Others: jQuery, Owl Carousel, Ajax


⚙️ Setup Instructions
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/youexcel-management-system.git
Create and activate a virtual environment:

bash
Copy
Edit
python -m venv .venv
.venv\Scripts\activate  # For Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run migrations:

bash
Copy
Edit
python manage.py migrate
Create a superuser:

bash
Copy
Edit
python manage.py createsuperuser
Start the development server:

bash
Copy
Edit
python manage.py runserver
