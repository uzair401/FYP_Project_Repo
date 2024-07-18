from django.db import models

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=128, unique=True)
    department_discipline = models.CharField(max_length=100)
    department_description = models.TextField()

    def __str__(self):
        return self.department_name

class Program(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_name = models.CharField(max_length=100, unique=True)
    program_code = models.CharField(max_length=50, unique=True)
    number_of_semesters = models.IntegerField()
    program_description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')

    def __str__(self):
        return self.program_name

class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    semester_number = models.IntegerField()
    semester_category = models.CharField(max_length=50)  # Fall or Spring
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='semesters')

    def __str__(self):
        return f"{self.semester_number} - {self.semester_category} - {self.program.program_name}"
    @property
    def semester_number_ordered(self):
        return f"{self.semester_number:02d}"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50, unique=True)
    credit_hours = models.IntegerField()
    internal_marks = models.IntegerField()
    mid_marks = models.IntegerField()
    final_marks = models.IntegerField()
    total_marks = models.IntegerField()
    course_description = models.TextField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.course_name

class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    batch_name = models.CharField(max_length=100, unique=True)
    batch_year = models.IntegerField()
    batch_number = models.IntegerField()
    batch_session = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='batches')

    def __str__(self):
        return self.batch_name