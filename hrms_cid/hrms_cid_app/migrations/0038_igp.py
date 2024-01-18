# Generated by Django 4.2.4 on 2024-01-05 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_cid_app', '0037_feedbackuser_division_feedbackuser_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Igp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hrms_cid_app.employees')),
            ],
        ),
    ]
