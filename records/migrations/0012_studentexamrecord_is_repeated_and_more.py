# Generated by Django 5.0.6 on 2024-08-10 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0011_remove_studentexamrecord_percentage_per_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentexamrecord',
            name='is_repeated',
            field=models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], default='No', max_length=3),
        ),
        migrations.AlterField(
            model_name='examrecord',
            name='record_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='studentexamrecord',
            name='total_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='studentsemesterrecord',
            name='semester_obtained_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='studentsemesterrecord',
            name='total_semester_marks',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]