# Generated by Django 4.2.4 on 2024-01-06 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_cid_app', '0039_employees_cpis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='district',
            field=models.CharField(max_length=50),
        ),
    ]