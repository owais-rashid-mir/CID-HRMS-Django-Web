# Generated by Django 4.2.4 on 2023-12-09 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_cid_app', '0029_remove_leavereportemployee_leave_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavereportemployee',
            name='special_dg_approval_status',
            field=models.IntegerField(default=0),
        ),
    ]
