import os

from django.contrib.auth.models import AbstractUser  # Admin User Model (Built-in Django User Model)
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from datetime import datetime

from django.db.models.signals import post_delete
from django.conf import settings


# using the Django's built-in AbstractUser model to create a custom user class and then creating two separate models (Admin and User) that link to the CustomUser model using OneToOneField.

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
    # If any section is deleted in Section table and that section was being used(via foreign key) in Supervisor table, we will simply set the deleted section as blank and null in the Supervisor. Other option is to use on_delete=models.CASCADE, but this will delete the entire row of data in Supervisor, which is NOT recommended and will result in data loss.
    section_id = models.ForeignKey(Sections, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()


# Ranks Model
class Rank(models.Model):
    rank_id = models.AutoField(primary_key=True)
    rank_name = models.CharField(max_length=50)
    description = models.TextField()
    objects = models.Manager()


# Division Model
class Divisions(models.Model):
    division_id = models.AutoField(primary_key=True)
    division_name = models.CharField(max_length=100)
    division_description = models.TextField()
    division_head = models.CharField(max_length=50)
    objects = models.Manager()


# Define a function to dynamically set the upload path for documents
def document_upload_path(instance, filename):
    # Get the current date in 'YYYY-MM-DD' format
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Combine the current date and the filename to create the upload path
    return os.path.join('document_upload_date_of_joining', current_date, filename)


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
    tehsil = models.TextField()
    district = models.TextField()
    parentage = models.TextField()
    mother_name = models.TextField()
    belt_no = models.TextField()
    pid_no = models.TextField()
    # date_joined = models.DateField()
    # null=True, blank=True : It allows the field to accept None and empty values, which is important since the field can be left empty. Otherwise, some Data error occurs if field is left empty.
    date_joined = models.DateField(null=True, blank=True)  # Date of joining in CID

    # Document File upload for Date of Joining In CID
    document_file = models.FileField(
        upload_to=document_upload_path,  # Define the upload path within your MEDIA_ROOT
        null=True,  # Set to True if the field can be left empty
        blank=True,  # Set to True if the field can be left blank in forms
    )

    date_appointment_police = models.DateField(null=True, blank=True)  # Date of appointment in police
    dob = models.DateField(null=True, blank=True)
    rank_id = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)
    aadhar_number = models.CharField(max_length=50, unique=True)
    pan_number = models.CharField(max_length=50, unique=True)
    previous_positions_held = models.TextField()
    qualifications = models.TextField()
    dialogue = models.TextField()
    adverse_report = models.TextField()
    section_id = models.ForeignKey(Sections, on_delete=models.SET_NULL, null=True, blank=True)
    division_id = models.ForeignKey(Divisions, on_delete=models.SET_NULL, null=True, blank=True)
    supervisor_id = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True)  # Use auto_now=True here, so whenever something is updated/edited, the updated_at time also changes.

    # Add the new field for Computer knowledge
    COMPUTER_CHOICES = [
        ('No', 'No'),
        ('Yes', 'Yes'),
    ]
    computer_knowledge = models.CharField(max_length=3, choices=COMPUTER_CHOICES, default='No', null=True, blank=True)

    # Add the fields for computer degree and skill level
    COMPUTER_DEGREE_CHOICES = [
        ('None', 'None'),
        ('Diploma', 'Diploma'),
        ('Degree', 'Degree'),
    ]
    computer_degree = models.CharField(max_length=7, choices=COMPUTER_DEGREE_CHOICES, default='None')

    COMPUTER_SKILL_CHOICES = [
        ('None', 'None'),
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Poor', 'Poor'),
    ]
    computer_skill = models.CharField(max_length=9, choices=COMPUTER_SKILL_CHOICES, default='None')

    objects = models.Manager()


class LeaveReportEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    # emp_id = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    leave_start_date = models.CharField(max_length=255)
    leave_end_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackUser(models.Model):
    id = models.AutoField(primary_key=True)
    # emp_id = models.ForeignKey(Staffs, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            User.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.user.save()
