# Generated by Django 5.0.6 on 2024-08-04 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0004_alter_batch_batch_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='batch_status',
            field=models.CharField(choices=[('active', 'Active'), ('passedout', 'Passed Out')], default='active', max_length=10),
        ),
    ]
