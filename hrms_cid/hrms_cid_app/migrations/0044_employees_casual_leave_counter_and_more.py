# Generated by Django 4.2.4 on 2024-01-10 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_cid_app', '0043_leavereportemployee_igp_approval_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='casual_leave_counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employees',
            name='casual_leave_reset_year',
            field=models.IntegerField(default=0),
        ),
    ]
