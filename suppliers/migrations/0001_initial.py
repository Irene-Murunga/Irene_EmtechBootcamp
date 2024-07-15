# Generated by Django 4.2.13 on 2024-06-14 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('businessName', models.CharField(max_length=255)),
                ('supplieridNO', models.CharField(max_length=255)),
                ('prefix', models.CharField(max_length=255)),
                ('firstname', models.CharField(max_length=255)),
                ('middlename', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('phoneNumber', models.CharField(max_length=255)),
                ('altPhone', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postalCode', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('openingBalance', models.FloatField()),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'suppliers',
            },
        ),
        migrations.CreateModel(
            name='SuppliersAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('supplier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='suppliers.suppliers')),
            ],
        ),
    ]
