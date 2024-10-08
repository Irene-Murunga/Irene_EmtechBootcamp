# Generated by Django 4.2.7 on 2024-07-11 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uniqueId', models.CharField(blank=True, max_length=50, unique=True)),
                ('admNumber', models.CharField(max_length=255)),
                ('schoolCode', models.CharField(blank=True, max_length=50, null=True)),
                ('firstName', models.CharField(max_length=255)),
                ('middleName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('studentGender', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('dateOfAdmission', models.DateField(auto_now_add=True)),
                ('healthStatus', models.CharField(blank=True, max_length=255, null=True)),
                ('grade', models.IntegerField()),
                ('stream', models.CharField(max_length=255)),
                ('schoolStatus', models.CharField(blank=True, max_length=255, null=True)),
                ('dormitory', models.CharField(blank=True, max_length=255, null=True)),
                ('parentID', models.IntegerField()),
                ('upiNumber', models.CharField(max_length=255)),
                ('urls', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='StudentAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='students.students')),
            ],
        ),
    ]
