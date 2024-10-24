# Generated by Django 5.0.6 on 2024-07-28 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('registration_number', models.CharField(max_length=100, unique=True)),
                ('enrollment_year', models.IntegerField()),
                ('status', models.CharField(choices=[('Enrolled', 'Enrolled'), ('Probation', 'Probation'), ('Semester Drop', 'Semester Drop'), ('Dropout', 'Dropout'), ('Pass Out', 'Pass Out')], max_length=50)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='academics.batch')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='academics.department')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_enrolled', to='academics.program')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('enrollment_id', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='students.student')),
            ],
        ),
    ]
