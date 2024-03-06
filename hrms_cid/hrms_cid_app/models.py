import os
from django.contrib.auth.models import AbstractUser  # Admin User Model (Built-in Django User Model)
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from datetime import datetime
from django.db.models.signals import post_delete
from django.conf import settings


# Security Question for Admin and User account signup - (NOT BEING USED BUT DON'T REMOVE IT.)
class AdminSecurityQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    objects = models.Manager()


class UserSecurityQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    objects = models.Manager()


# Division Model
class Divisions(models.Model):
    division_id = models.AutoField(primary_key=True)
    division_name = models.CharField(max_length=100)
    division_description = models.TextField()
    division_head = models.CharField(max_length=50)     # Not being used. fetched from DivisionHead table in HTML file.
    objects = models.Manager()


# Section Model
class Sections(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=100)
    description = models.TextField()
    section_incharge = models.CharField(max_length=50)      # Not being used.
    # Add a ForeignKey to establish the relationship between Sections and Divisions
    division = models.ForeignKey(Divisions, on_delete=models.CASCADE)
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
    district = models.CharField(max_length=50)
    parentage = models.TextField()
    mother_name = models.TextField()
    belt_no = models.TextField()
    pid_no = models.TextField()
    cpis = models.TextField()
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

    previous_positions_held_within_cid = models.TextField()
    previous_positions_held_outside_cid = models.TextField()

    qualifications = models.TextField()

    DIALOGUE_CHOICES = [
        ('Null', 'Null'),
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Average', 'Average'),
    ]
    dialogue = models.CharField(max_length=9, choices=DIALOGUE_CHOICES, default='Null')

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

    previous_trainings_done = models.TextField()

    other_emp_info = models.TextField(null=True, blank=True)

    # Leave Counters
    casual_leave_counter = models.IntegerField(default=0)
    # casual_leave_reset_year = models.IntegerField(default=0)    # For resetting the leave counter at the start of new year.
    earned_leave_counter = models.IntegerField(default=0)
    paternity_maternity_leave_counter = models.IntegerField(default=0)
    committed_leave_counter = models.IntegerField(default=0)

    objects = models.Manager()


# using the Django's built-in AbstractUser model to create a custom user class and then creating 7 separate models that link to the CustomUser model using OneToOneField.
class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "User"), (3, "Section Head"), (4, "Division Head"), (5, "DDO"), (6, "Special DG"), (7, "IGP"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

    admin_security_question = models.ForeignKey(
        AdminSecurityQuestion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_users'
    )
    user_security_question = models.ForeignKey(
        UserSecurityQuestion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_users'
    )

    # Use email as the username
    username = models.EmailField(unique=True)

    # Add an email field
    email = models.EmailField(unique=True)

    # Add a reference to the Employee model
    employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.email


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class User(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class SectionHead(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.ForeignKey(Sections, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class DivisionHead(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    division = models.ForeignKey(Divisions, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Ddo(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class SpecialDg(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Igp(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    # employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    pid = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    leave_start_date = models.CharField(max_length=255)
    leave_end_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_type = models.CharField(max_length=255)  # Example: Casual, Earned, Paternity/Maternity, Committed
    rank = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    division = models.CharField(max_length=50)

    section_head_approval_status = models.IntegerField(default=0)
    division_head_approval_status = models.IntegerField(default=0)
    ddo_approval_status = models.IntegerField(default=0)
    igp_approval_status = models.IntegerField(default=0)
    special_dg_approval_status = models.IntegerField(default=0)

    # leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    pid = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# Profile Correction Request
class ProfileCorrReq(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    pid = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    corr_req_msg = models.TextField()

    # column_name, current_value, correct_value are not being used right now.
    column_name = models.CharField(max_length=50)  # New field for column name where data is incorrect.
    current_value = models.TextField()  # New field for current value
    correct_value = models.TextField()  # New field for correct value

    corr_req_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class ArchivedEmployees(models.Model):
    emp_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_pic = models.FileField()
    gender = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    tehsil = models.TextField()
    district = models.CharField(max_length=50)
    parentage = models.TextField()
    mother_name = models.TextField()
    belt_no = models.TextField()
    pid_no = models.TextField()
    cpis = models.TextField()
    date_joined = models.DateField(null=True, blank=True)
    document_file = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    date_appointment_police = models.DateField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    rank_id = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)
    aadhar_number = models.CharField(max_length=50, unique=True)
    pan_number = models.CharField(max_length=50, unique=True)
    previous_positions_held_within_cid = models.TextField()
    previous_positions_held_outside_cid = models.TextField()
    qualifications = models.TextField()
    dialogue = models.CharField(max_length=9, default='Null')
    adverse_report = models.TextField()
    section_id = models.ForeignKey(Sections, on_delete=models.SET_NULL, null=True, blank=True)
    division_id = models.ForeignKey(Divisions, on_delete=models.SET_NULL, null=True, blank=True)
    supervisor_id = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    computer_knowledge = models.CharField(max_length=3, default='No', null=True, blank=True)
    computer_degree = models.CharField(max_length=7, default='None')
    computer_skill = models.CharField(max_length=9, default='None')
    previous_trainings_done = models.TextField()
    other_emp_info = models.TextField(null=True, blank=True)
    archived_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            # Admin.objects.create(admin=instance)
            Admin.objects.create(admin=instance, employee=instance.employee)
        elif instance.user_type == 2:
            #User.objects.create(user=instance)
            User.objects.create(admin=instance, employee=instance.employee)
        elif instance.user_type == 3:
            SectionHead.objects.create(admin=instance, employee=instance.employee)
        elif instance.user_type == 4:
            DivisionHead.objects.create(admin=instance, employee=instance.employee)
        elif instance.user_type == 5:
            Ddo.objects.create(admin=instance, employee=instance.employee)
        elif instance.user_type == 6:
            SpecialDg.objects.create(admin=instance, employee=instance.employee)
        elif instance.user_type == 7:
            Igp.objects.create(admin=instance, employee=instance.employee)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    elif instance.user_type == 2:
        instance.user.save()
    elif instance.user_type == 3:
        instance.sectionhead.save()
    elif instance.user_type == 4:
        instance.divisionhead.save()
    elif instance.user_type == 5:
        instance.ddo.save()
    elif instance.user_type == 6:
        instance.specialdg.save()
    elif instance.user_type == 7:
        instance.igp.save()
