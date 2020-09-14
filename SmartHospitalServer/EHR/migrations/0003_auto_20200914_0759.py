# Generated by Django 3.1 on 2020-09-14 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_patient_is_validated'),
        ('EHR', '0002_auto_20200914_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill_entry',
            name='patient',
            field=models.ForeignKey(default=1, limit_choices_to={'is_validated': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.patient'),
        ),
        migrations.AlterField(
            model_name='medhistory_entry',
            name='patient',
            field=models.ForeignKey(default=1, limit_choices_to={'is_validated': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.patient'),
        ),
        migrations.AlterField(
            model_name='prescription_entry',
            name='patient',
            field=models.ForeignKey(default=1, limit_choices_to={'is_validated': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.patient'),
        ),
    ]
