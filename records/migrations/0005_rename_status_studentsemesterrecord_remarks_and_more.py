# Generated by Django 5.0.6 on 2024-08-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_alter_examrecord_exam_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentsemesterrecord',
            old_name='status',
            new_name='remarks',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='batch',
        ),
        migrations.AddField(
            model_name='examrecord',
            name='session',
            field=models.CharField(choices=[('Fall', 'Fall'), ('Spring', 'Spring')], default='Fall', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentexamrecord',
            name='remarks',
            field=models.CharField(default='Pass', max_length=50),
            preserve_default=False,
        ),
    ]
