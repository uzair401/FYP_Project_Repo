from django.db import models
from django.contrib.auth.models import User
from academics.models import Program, Batch, Semester, Course
from students.models import Student

class ExamRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    record_name = models.CharField(max_length=100)
    record_year = models.IntegerField()
    examiner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_records')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='exam_records')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='exam_records')

    def __str__(self):
        return self.record_name

class StudentExamRecord(models.Model):
    student_exam_rec_id = models.AutoField(primary_key=True)
    internal_marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    mid_marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    final_marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    percentage_per_course = models.DecimalField(max_digits=5, decimal_places=2)
    gpa_per_course = models.DecimalField(max_digits=5, decimal_places=2)
    exam_record = models.ForeignKey(ExamRecord, on_delete=models.CASCADE, related_name='student_exam_records')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='student_exam_records')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='student_exam_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_exam_records')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='student_exam_records')

    def __str__(self):
        return f"Student Exam Record {self.student_exam_rec_id}"

class StudentSemesterRecord(models.Model):
    total_semester_marks = models.DecimalField(max_digits=5, decimal_places=2)
    semester_obtained_marks = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    gpa_per_semester = models.DecimalField(max_digits=5, decimal_places=2)
    cgpa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, choices=Student.STUDENT_STATUS_CHOICES)
    student_exam_rec = models.OneToOneField(StudentExamRecord, on_delete=models.CASCADE, related_name='semester_record')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='semester_records')

    def __str__(self):
        return f"Student Semester Record {self.id}"
