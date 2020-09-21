# Generated by Django 3.1 on 2020-09-17 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_patient_is_validated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient_Health',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.DecimalField(decimal_places=3, max_digits=5)),
                ('recorded_time', models.DateTimeField(auto_now_add=True)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
        ),
    ]
