# Generated by Django 4.2.7 on 2024-07-14 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transaction_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='tran_category',
            field=models.CharField(max_length=200),
        ),
    ]
