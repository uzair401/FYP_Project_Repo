# Generated by Django 5.0.6 on 2024-07-31 12:14

import records.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_alter_studentexamrecord_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentexamrecord',
            name='final_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[records.models.validate_percentage]),
        ),
        migrations.AlterField(
            model_name='studentexamrecord',
            name='gpa_per_course',
            field=models.DecimalField(decimal_places=2, max_digits=3, validators=[records.models.validate_gpa]),
        ),
        migrations.AlterField(
            model_name='studentexamrecord',
            name='internal_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[records.models.validate_percentage]),
        ),
        migrations.AlterField(
            model_name='studentexamrecord',
            name='mid_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[records.models.validate_percentage]),
        ),
        migrations.AlterField(
            model_name='studentexamrecord',
            name='percentage_per_course',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[records.models.validate_percentage]),
        ),
        migrations.AlterField(
            model_name='studentsemesterrecord',
            name='cgpa',
            field=models.DecimalField(decimal_places=2, max_digits=3, validators=[records.models.validate_gpa]),
        ),
        migrations.AlterField(
            model_name='studentsemesterrecord',
            name='gpa_per_semester',
            field=models.DecimalField(decimal_places=2, max_digits=3, validators=[records.models.validate_gpa]),
        ),
        migrations.AlterField(
            model_name='studentsemesterrecord',
            name='percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[records.models.validate_percentage]),
        ),
        migrations.AlterField(
            model_name='studentsemesterrecord',
            name='semester_obtained_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[records.models.validate_percentage]),
        ),
        migrations.AlterField(
            model_name='studentsemesterrecord',
            name='total_semester_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[records.models.validate_percentage]),
        ),
    ]
