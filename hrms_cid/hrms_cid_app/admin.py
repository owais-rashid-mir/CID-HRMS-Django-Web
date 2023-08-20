from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from hrms_cid_app.models import CustomUser  # CustomUser is defined in models.py


# Creating blank user model- if this is not done, password won't be encrypted.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
