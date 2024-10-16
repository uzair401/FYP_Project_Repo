##Examination Management System (EMS)

Overview
The Examination Management System (EMS) is a web application designed to facilitate the management of examination-related activities in educational institutions. 
This system enables users to manage students, academic records, examination schedules, and results efficiently.

Features
- User Authentication: Secure login for students and administrators.
- Student Management: Add, update, and view student profiles and their academic records.
- Examination Management: Schedule exams, assign subjects, and manage results.
- Admin Dashboard: Comprehensive interface for administrators to oversee all operations.
- Reports Generation: Generate reports for student performance and examination statistics.

Technologies Used
- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (default) / PostgreSQL
- Others: Bootstrap for styling, Django Rest Framework for APIs

Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/uzair401/FYP_Project_Repo.git
   cd FYP_Project_Repo
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application: Open your web browser and navigate to `http://127.0.0.1:8000`.

Folder Structure
```plaintext
FYP_Project_Repo/
│
├── ERMS_System/              Core project settings and configurations
│   ├── __init__.py
│   ├── settings.py           Project settings
│   ├── urls.py               URL routing
│   └── wsgi.py               WSGI configuration for deployment
│
├── students/                 Application managing student data
│   ├── migrations/           Database migrations for students app
│   ├── admin.py              Admin panel configurations
│   ├── models.py             Student models
│   ├── views.py              Views for handling requests
│   └── templates/            HTML templates for student management
│
├── academics/                Application managing academic records
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── templates/
│
├── records/                  Application for managing examination records
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── templates/
│
├── templates/                Global templates for the project
├── requirements.txt          List of project dependencies
└── manage.py                 Django management script
```

Module Descriptions
ERMS_System
- **settings.py**: Contains all configuration settings for the Django project, including database configuration, middleware, static files, and installed apps.
- **urls.py**: Manages URL routing for the application. It directs incoming requests to appropriate views based on the requested URL.
- **wsgi.py**: Configuration file for WSGI, allowing the application to communicate with web servers for deployment.

Students Module
- **admin.py**: Registers the student models with the Django admin interface for easy management. Administrators can add, edit, and delete student records through this interface.
- **models.py**: Defines the data models for students, including fields such as name, roll number, date of birth, and enrollment status. Each model corresponds to a table in the database.
- **views.py**: Contains logic for handling requests related to student data. This includes creating new student records, displaying student details, and listing all students.
- **templates/**: Contains HTML templates for student management views, rendering dynamic content for student-related operations.

Academics Module
- **admin.py**: Configures the admin interface for managing academic records, enabling the addition and editing of subjects and courses.
- **models.py**: Defines models for academic entities such as subjects and courses, including fields for subject names and codes.
- **views.py**: Handles requests related to academic records, allowing for CRUD operations on subjects and courses.
- **templates/**: HTML templates for academic record management, providing user interfaces for managing subjects.

Records Module
- **admin.py**: Registers examination records and results with the Django admin interface, facilitating easy access and management.
- **models.py**: Contains models for examination records, including fields for exam dates, subjects, and student results.
- **views.py**: Implements functionality for managing examination records, allowing administrators to schedule exams and record results.
- **templates/**: Provides HTML templates for displaying and managing examination records and results.

Global Templates
- **templates/**: Contains global templates that can be shared across different modules, enhancing the consistency and reusability of the user interface.

Usage
1. **Login as Admin**: Use the provided admin credentials to manage the system.
2. **Manage Students**: Add or update student records through the student management interface.
3. **Schedule Exams**: Use the examination management features to set up and manage exam schedules.
4. **View Reports**: Generate and view performance reports for students.

Contribution
Contributions to this project are welcome! If you want to add features or fix bugs, please fork the repository and submit a pull request.

License
This project is licensed under the MIT License.
