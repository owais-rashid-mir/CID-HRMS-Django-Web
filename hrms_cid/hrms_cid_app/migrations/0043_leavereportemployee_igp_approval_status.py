# Generated by Django 4.2.4 on 2024-01-07 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_cid_app', '0042_sections_division'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavereportemployee',
            name='igp_approval_status',
            field=models.IntegerField(default=0),
        ),
    ]
