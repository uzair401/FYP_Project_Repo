from django.db import models
from core.models import User  # Import the User model from core
from academics.models import Department, Program, Semester, Course, Batch

class Student(models.Model):
    STUDENT_STATUS_CHOICES = (
        ('Enrolled', 'Enrolled'),
        ('Probation', 'Probation'),
        ('Semester Drop', 'Semester Drop'),
        ('Dropout', 'Dropout'),
        ('Pass Out', 'Pass Out'),
    )
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    registration_number = models.CharField(max_length=100, unique=True)
    enrollment_year = models.IntegerField()
    status = models.CharField(max_length=50, choices=STUDENT_STATUS_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='students_enrolled')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def current_semester(self):
        # Logic to determine the current semester for the student
        # You may implement this based on your application's requirements
        pass

class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"Enrollment {self.enrollment_id}"
