# Generated by Django 4.2.4 on 2023-12-11 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_cid_app', '0033_profilecorrreq'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profilecorrreq',
            old_name='corr_req',
            new_name='corr_req_msg',
        ),
    ]
