# Generated by Django 4.2.4 on 2023-12-11 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_cid_app', '0031_leavereportemployee_division_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='other_emp_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]