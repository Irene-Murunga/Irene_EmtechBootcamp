# Generated by Django 3.2.10 on 2024-08-09 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeextensions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeextensions',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
