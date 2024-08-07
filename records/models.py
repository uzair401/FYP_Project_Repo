from django.db import models
from django.core.exceptions import ValidationError
from core.models import User
from academics.models import Batch, Semester
# Custom validation for GPA and percentages
def validate_percentage(value):
    if not (0 <= value <= 100):
        raise ValidationError('Percentage must be between 0 and 100.')

def validate_gpa(value):
    if not (0 <= value <= 4.0):
        raise ValidationError('GPA must be between 0 and 4.0.')

class ExamRecord(models.Model):
    SESSION_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
    ]
    record_id = models.AutoField(primary_key=True)
    record_name = models.CharField(max_length=255, unique=True)
    record_year = models.IntegerField()
    exam_date = models.DateField()
    session = models.CharField(max_length=10, choices=SESSION_CHOICES) 
    examiner = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey('academics.Program', on_delete=models.CASCADE)
    def save(self, *args, **kwargs):    
        self.record_name = self.record_name.upper()
        super(ExamRecord, self).save(*args, **kwargs)
    class Meta:
        unique_together = ('record_name', 'record_year', 'exam_date')  # Assuming this combination should be unique
    def __str__(self):
        return f"{self.record_name} ({self.session})"

class StudentExamRecord(models.Model):
    GRADE_CHOICES = [
        ('F', 'F'),
        ('C-', 'C-'),
        ('C+', 'C+'),
        ('B-', 'B-'),
        ('B', 'B'),
        ('B+', 'B+'),
        ('A-', 'A-'),
        ('A', 'A'),
        ('A+', 'A+'),
    ]
    student_exam_rec_id = models.AutoField(primary_key=True)
    internal_marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_percentage])
    mid_marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_percentage] )
    final_marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_percentage] )
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_percentage] )
    gpa_per_course = models.DecimalField(max_digits=3, decimal_places=2, validators=[validate_gpa] )
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    remarks = models.CharField(max_length=50)
    exam_record = models.ForeignKey(ExamRecord, on_delete=models.CASCADE)
    program = models.ForeignKey('academics.Program', on_delete=models.CASCADE)
    semester = models.ForeignKey('academics.Semester', on_delete=models.CASCADE)
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('exam_record', 'student', 'course')  # Unique per exam record, student, and course

class StudentSemesterRecord(models.Model):
    student_exam_rec = models.ForeignKey(StudentExamRecord, on_delete=models.CASCADE)
    total_semester_marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_percentage])
    semester_obtained_marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_percentage])
    percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_percentage])
    gpa_per_semester = models.DecimalField(max_digits=3, decimal_places=2, validators=[validate_gpa] )
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, validators=[validate_gpa] )
    remarks = models.CharField(max_length=50)
    exam_record = models.ForeignKey(ExamRecord, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    semester = models.ForeignKey('academics.Semester', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'semester', 'exam_record')  # Unique per student, semester, and exam record

class ExamEnrollment(models.Model):
    exam_record = models.ForeignKey(ExamRecord, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # Add other fields if necessary
    
    class Meta:
        unique_together = ('exam_record', 'batch', 'semester')  # Ensure this matches your requirements

    def __str__(self):
        return f"{self.exam_record} - {self.batch} - {self.semester}"