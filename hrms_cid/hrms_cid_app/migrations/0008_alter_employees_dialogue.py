# Generated by Django 4.2.4 on 2023-10-08 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_cid_app', '0007_alter_employees_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='dialogue',
            field=models.CharField(choices=[('Null', 'Null'), ('Excellent', 'Excellent'), ('Good', 'Good'), ('Average', 'Average')], default='Null', max_length=9),
        ),
    ]
