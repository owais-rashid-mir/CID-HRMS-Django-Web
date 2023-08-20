from django.contrib.auth.models import AbstractUser  # Admin User Model (Built-in Django User Model)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "User"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class User(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# Section Model
class Sections(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=100)
    description = models.TextField()
    section_incharge = models.CharField(max_length=50)
    objects = models.Manager()


# Supervisor Model
class Supervisor(models.Model):
    supervisor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    objects = models.Manager()


# Employee model
class Employees(models.Model):
    emp_id = models.AutoField(primary_key=True)
    # admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_pic = models.FileField()
    gender = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    date_joined = models.DateField()
    position = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=50, unique=True)
    pan_number = models.CharField(max_length=50, unique=True)
    previous_positions_held = models.TextField()
    qualifications = models.TextField()
    computer_knowledge = models.TextField()
    dialogue = models.TextField()
    adverse_report = models.TextField()
    section_id = models.ForeignKey(Sections, on_delete=models.DO_NOTHING)
    supervisor_id = models.ForeignKey(Supervisor, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            User.objects.create(admin=instance, address="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.user.save()
