# Generated by Django 3.2.10 on 2024-04-25 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_rename_parentid_students_parentidno'),
    ]

    operations = [
        migrations.RenameField(
            model_name='students',
            old_name='schoolID',
            new_name='schools',
        ),
    ]
