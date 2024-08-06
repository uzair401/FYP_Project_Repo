# Generated by Django 5.0.6 on 2024-08-06 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0009_alter_studentexamrecord_percentage_per_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentexamrecord',
            name='grade',
            field=models.CharField(choices=[('F', 'F'), ('C-', 'C-'), ('C+', 'C+'), ('B-', 'B-'), ('B', 'B'), ('B+', 'B+'), ('A-', 'A-'), ('A', 'A'), ('A+', 'A+')], default='F', max_length=10),
            preserve_default=False,
        ),
    ]