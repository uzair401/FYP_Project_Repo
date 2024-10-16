# Examination Management System (EMS)

## Overview
The Examination Management System (EMS) is a web application designed to facilitate the management of examination-related activities in educational institutions specefically for College and Universities. 
This system enables users to manage students, academic records, examination records, and results efficiently.

## Features
- User Authentication: Secure login process for Faculty and Administrators to ensure that only authorized personnel can access sensitive information.

- Role-Based Access: A structured approach to data access based on user roles, including Admin, Faculty, and Editors, ensuring appropriate permissions for each role.

- Academic Data Management: Facilitates the addition, updating, and viewing of records related to Departments, Programs, Courses, Batches, and Students, ensuring accurate and up-to-date information.

- Examination Management: Allows the creation, updating, and viewing of exam records according to the academic year, streamlining the examination process.

- Results and Reports: Manages hierarchical results, providing individual course results, semester results, and student transcripts for respective batches in programs.

- User Management: Oversees user accounts, creating roles for Editors with view and update access to specific data, Faculty with department-level access, and Administrators with comprehensive system-level access.

## Technologies Used
- Backend: Python, Django
- Frontend: HTML, CSS, JavaScript, using the AdminLTE 3 framework for enhanced styling.
- Database: PostgreSQL
- Others: AdminLTE 3 Bootstrap Theme for consistent and responsive design.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/uzair401/FYP_Project_Repo.git
   cd FYP_Project_Repo
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup Permissions:
   ```bash
   python manage.py setup_groups_and_permissions
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

## Folder Structure
```
FYP_Project_Repo/
│
├── ERMS_System/              # Core project settings and configurations
│   ├── __init__.py
│   ├── settings.py           # Project settings and configurations
│   ├── urls.py               # URL routing for the project
│   ├── wsgi.py               # WSGI configuration for deployment
│   └── asgi.py               # ASGI configuration (if applicable)
│
├── students/                 # Application for managing student data
│   ├── migrations/           # Database migrations for the students app
│   ├── admin.py              # Admin panel configurations for student management
│   ├── models.py             # Data models related to students
│   ├── views.py              # Views for handling student-related requests
│   ├── forms.py              # Forms for student data input (if applicable)
│
├── academics/                # Application for managing academic records
│   ├── migrations/
│   ├── admin.py              # Admin configurations for academic records
│   ├── models.py             # Data models for academic entities (subjects, courses, etc.)
│   ├── views.py              # Views for academic record operations
│   ├── forms.py              # Forms for academic data input (if applicable)
│
├── records/                  # Application for managing examination records
│   ├── migrations/
│   ├── admin.py              # Admin configurations for examination records
│   ├── models.py             # Data models for exams and results
│   ├── views.py              # Views for managing examination records
│   ├── forms.py              # Forms for exam data input (if applicable)
│
├── templates/                # Global templates for the project
│   ├── base.html             # Base template for extending other templates
│   ├── Core/                 # Subdirectory for core functionalities related templates
│   ├── students/             # Subdirectory for student-related templates
│   ├── academics/            # Subdirectory for academic-related templates
│   └── records/              # Subdirectory for examination-related templates
│
├── requirements.txt          # List of project dependencies
└── manage.py                 # Django management script
```



## Module Descriptions
### ERMS_System
- **settings.py**: Contains all configuration settings for the Django project, including database configuration, middleware, static files, and installed apps.
- **urls.py**: Manages URL routing for the application. It directs incoming requests to appropriate views based on the requested URL.
- **wsgi.py**: Configuration file for WSGI, allowing the application to communicate with web servers for deployment.

### Students Module
- **admin.py**: Registers the student models with the Django admin interface for easy management. Administrators can add, edit, and delete student records through this interface.
- **models.py**: Defines the data models for students, including fields such as name, roll number, date of birth, and enrollment status. Each model corresponds to a table in the database.
- **views.py**: Contains logic for handling requests related to student data. This includes creating new student records, displaying student details, and listing all students.
- **forms.py**: Defines forms for student-related data input and validation, allowing users to create and update student records through structured forms.

### Academics Module
- **admin.py**: Configures the admin interface for managing academic records, enabling the addition and editing of subjects and courses.
- **models.py**: Defines models for academic entities such as subjects and courses, including fields for subject names and codes.
- **views.py**: Handles requests related to academic records, allowing for CRUD operations on subjects and courses.
- **forms.py**: Contains forms for inputting and validating academic data, facilitating structured data entry for subjects and courses.

### Records Module
- **admin.py**: Registers examination records and results with the Django admin interface, facilitating easy access and management.
- **models.py**: Contains models for examination records, including fields for exam dates, subjects, and student results.
- **views.py**: Implements functionality for managing examination records, allowing administrators to schedule exams and record results.
- **forms.py**: Defines forms for managing examination data, ensuring proper validation and input for exam records.

### Global Templates
- **templates/**: Contains global templates that can be shared across different modules, enhancing the consistency and reusability of the user interface.

### Templates Directory
- **templates/**
  - **students/**
    - `student_list.html`
    - `student_detail.html`
    - `student_form.html`
  
  - **academics/**
    - `subject_list.html`
    - `subject_detail.html`
    - `subject_form.html`

  - **records/**
    - `exam_list.html`
    - `exam_detail.html`
    - `exam_form.html`


## Usage
1. **Login as Admin**: Use the provided admin credentials to manage the system.
2. **Manage Students**: Add or update student records through the student management interface.
3. **Schedule Exams**: Use the examination management features to set up and manage exam schedules.
4. **View Reports**: Generate and view performance reports for students.

## Contribution
Contributions to this project are welcome! If you want to add features or fix bugs, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
