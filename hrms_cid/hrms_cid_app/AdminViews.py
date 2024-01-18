# Contains the logic for Admin-side functionality and features.

import datetime
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.contrib.auth.hashers import make_password
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import uuid  # uuid module for generating unique identifiers that can be appended with file names.

from hrms_cid_app.models import CustomUser, User, Sections, Supervisor, Employees, FeedBackUser, LeaveReportEmployee, \
    Rank, Divisions, AdminSecurityQuestion, UserSecurityQuestion, SectionHead, DivisionHead, ProfileCorrReq, Admin, Ddo, \
    SpecialDg, Igp, ArchivedEmployees


def admin_home(request):
    # For fetching the count on Admin homepage(home_content.html)
    employee_count = Employees.objects.all().count()
    division_count = Divisions.objects.all().count()
    section_count = Sections.objects.all().count()
    rank_count = Rank.objects.all().count()

    return render(request, "admin_template/home_content.html",{"employee_count":employee_count,"division_count":division_count, "section_count":section_count,"rank_count":rank_count} )


# ------------------------------- Admin Login---------------------------------------
# Add Admin login
def add_admin(request):
    employees = Employees.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, "admin_template/add_admin_template.html", context)


# Taking FORM data from add_admin_template.html, processing it, and storing it in the database.
def add_admin_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        # email etc is the name of form input field in add_admin_template.html
        emp_id = request.POST.get("employee")
        password = request.POST.get("password")

        # Validate password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("add_admin"))

        # Validate if password contains any whitespace
        if ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("add_admin"))

        # Use get_object_or_404 to handle the case where the employee does not exist
        employee = get_object_or_404(Employees, emp_id=emp_id)

        try:
            # CustomUser is defined in models.py.
            # Giving this user some admin access. Storing in CustomUser table which has the login
            # ... credentials of Admin as well as User. For Admin, user_type=1   .
            # ... For User, user_type=2
            admin_login = CustomUser.objects.create_user(username=employee.email, email=employee.email, password=password, employee=employee, user_type=1)

            admin_login.save()

            messages.success(request, "Successfully Added Admin Login")
            return HttpResponseRedirect(reverse("add_admin"))  # Once data is added, return to add_admin page.

        except Exception as e:
            messages.error(request, f"Failed To Add Admin Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("add_admin"))


# Manage Admins
def manage_admin(request):
    # Reading all Admin data by calling admin.objects.all(). Order the admin data by the date it was added.
    admin = Admin.objects.all().order_by('-created_at')
    return render(request, "admin_template/manage_admin_template.html", {"admin": admin})


# Edit admin login
def edit_admin(request, id):
    admin = get_object_or_404(CustomUser, id=id)
    employees = Employees.objects.all()

    context = {
        'admin': admin,
        'employees': employees,
    }
    return render(request, "admin_template/edit_admin_template.html", context)


# Update email and password in the database
def edit_admin_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        id = request.POST.get("id")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validate password length only if a new password is provided
        if password and len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("edit_admin", args=(id,)))

        # Validate if password contains any whitespace only if a new password is provided
        if password and ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("edit_admin", args=(id,)))

        admin = get_object_or_404(CustomUser, id=id)

        try:
            # Update email
            admin.email = email
            admin.username = email  # Set username the same as email

            # Update password only if a new password is provided
            if password:
                admin.set_password(password)

            admin.save()

            messages.success(request, "Successfully Updated Admin Login")
            return HttpResponseRedirect(reverse("edit_admin", args=(id,)))

        except Exception as e:
            messages.error(request, f"Failed To Update Admin Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("edit_admin", args=(id,)))


# Delete admin
def delete_admin(request, id):
    admin = get_object_or_404(CustomUser, id=id)

    try:
        admin.delete()
        messages.success(request, "Admin Login Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Failed to delete Admin Login. Error: {str(e)}")

    return HttpResponseRedirect(reverse("manage_admin"))


# ------------------------------- User Login---------------------------------------
# Add User login
def add_user(request):
    employees = Employees.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, "admin_template/add_user_template.html", context)


def add_user_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        # email etc is the name of form input field in add_user_template.html
        emp_id = request.POST.get("employee")
        password = request.POST.get("password")

        # Validate password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("add_user"))

        # Validate if password contains any whitespace
        if ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("add_user"))

        # Use get_object_or_404 to handle the case where the employee does not exist
        employee = get_object_or_404(Employees, emp_id=emp_id)

        try:
            # CustomUser is defined in models.py.
            # Giving this user some admin access. Storing in CustomUser table which has the login
            # ... credentials of Admin as well as User. For Admin, user_type=1   .
            # ... For User, user_type=2
            user = CustomUser.objects.create_user(username=employee.email, email=employee.email, password=password, employee=employee, user_type=2)

            user.save()

            messages.success(request, "Successfully Added User/Employee Login")
            return HttpResponseRedirect(reverse("add_user"))  # Once data is added, return to add_user page.

        except Exception as e:
            messages.error(request, f"Failed To Add User/Employee Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("add_user"))


# Manage Users
def manage_user(request):
    # Reading all User data by calling user.objects.all()
    user = User.objects.all().order_by('-created_at')
    return render(request, "admin_template/manage_user_template.html", {"user": user})


# Edit User login
def edit_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    employees = Employees.objects.all()

    context = {
        'user': user,
        'employees': employees,
    }
    return render(request, "admin_template/edit_user_template.html", context)


# Update email and password in the database
def edit_user_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        id = request.POST.get("id")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validate password length only if a new password is provided
        if password and len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("edit_user", args=(id,)))

        # Validate if password contains any whitespace only if a new password is provided
        if password and ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("edit_user", args=(id,)))

        user = get_object_or_404(CustomUser, id=id)

        try:
            # Update email
            user.email = email
            user.username = email  # Set username the same as email

            # Update password only if a new password is provided
            if password:
                user.set_password(password)

            user.save()

            messages.success(request, "Successfully Updated User/Employee Login")
            return HttpResponseRedirect(reverse("edit_user", args=(id,)))

        except Exception as e:
            messages.error(request, f"Failed To Update User/Employee Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("edit_user", args=(id,)))


# Delete user
def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)

    try:
        user.delete()
        messages.success(request, "User/Employee Login Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Failed to delete User/Employee Login. Error: {str(e)}")

    return HttpResponseRedirect(reverse("manage_user"))


# ------------------------------- Section Head Login---------------------------------------
# Add section login
def add_section_head(request):
    sections = Sections.objects.all()
    employees = Employees.objects.all()
    context = {
        'sections': sections,
        'employees': employees,
    }
    return render(request, "admin_template/add_section_head_template.html", context)


def add_section_head_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        emp_id = request.POST.get("employee")
        password = request.POST.get("password")

        # Validate password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("add_section_head"))

        # Validate if password contains any whitespace
        if ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("add_section_head"))

        employee = get_object_or_404(Employees, emp_id=emp_id)

        try:
            section_head, created = SectionHead.objects.get_or_create(
                employee=employee,
                defaults={'admin': CustomUser.objects.create_user(
                    email=employee.email,
                    username=employee.email,
                    password=make_password(password),  # Use make_password to hash the password
                    employee=employee,
                    user_type=3
                )}
            )

            if not created:
                section_head.admin.password = make_password(password)
                section_head.admin.save()

                messages.success(request, "Successfully Added/Updated Section Head Login")
            else:
                messages.success(request, "Successfully Added Section Head Login")

            # Set the section for the SectionHead
            section_head.section = employee.section_id
            section_head.save()

            return HttpResponseRedirect(reverse("add_section_head"))

        except Exception as e:
            messages.error(request, f"Failed To Add/Update Section Head Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("add_section_head"))


# Manage Section Head
def manage_section_head(request):
    section_head = SectionHead.objects.all().order_by('-created_at')
    return render(request, "admin_template/manage_section_head_template.html", {"section_head": section_head})


# Edit Section Head login
def edit_section_head(request, admin_id):
    section_head = get_object_or_404(SectionHead, admin__id=admin_id)
    sections = Sections.objects.all()
    context = {
        'section_head': section_head,
        'sections': sections,
    }
    return render(request, "admin_template/edit_section_head_template.html", context)


def edit_section_head_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        admin_id = request.POST.get("admin_id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        section_id = request.POST.get("section")

        try:
            section_head = SectionHead.objects.get(admin__id=admin_id)
            section_head.admin.email = email

            # Set username as email
            section_head.admin.username = email

            # Check if the password is provided for updating
            if password:
                # Validate password length
                if len(password) < 8:
                    messages.error(request, "Password must be at least 8 characters or longer.")
                    return HttpResponseRedirect(reverse("edit_section_head", args=[admin_id]))

                # Validate if password contains any whitespace
                if ' ' in password:
                    messages.error(request, "Password cannot contain any spaces.")
                    return HttpResponseRedirect(reverse("edit_section_head", args=[admin_id]))

                section_head.admin.password = make_password(password)   # make_password for hashing

            # Update the section
            section_head.section = Sections.objects.get(section_id=section_id)

            # Save the changes
            section_head.admin.save()
            section_head.save()

            messages.success(request, "Successfully updated Section Head details")
            return HttpResponseRedirect(reverse("edit_section_head", args=[admin_id]))

        except Exception as e:
            messages.error(request, f"Failed to update Section Head details. Error: {str(e)}")
            return HttpResponseRedirect(reverse("edit_section_head", args=[admin_id]))


# Delete Section Head
def delete_section_head(request, id):
    section_head = get_object_or_404(CustomUser, id=id)

    try:
        section_head.delete()
        messages.success(request, "Section Head Login Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Failed to delete Section Head Login. Error: {str(e)}")

    return HttpResponseRedirect(reverse("manage_section_head"))


# ------------------------------- Division Head Login---------------------------------------
# Add division login
def add_division_head(request):
    divisions = Divisions.objects.all()
    employees = Employees.objects.all()
    context = {
        'divisions': divisions,
        'employees': employees,
    }
    return render(request, "admin_template/add_division_head_template.html", context)


def add_division_head_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        emp_id = request.POST.get("employee")
        password = request.POST.get("password")

        # Validate password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("add_division_head"))

        # Validate if password contains any whitespace
        if ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("add_division_head"))

        employee = get_object_or_404(Employees, emp_id=emp_id)

        try:
            division_head, created = DivisionHead.objects.get_or_create(
                employee=employee,
                defaults={'admin': CustomUser.objects.create_user(
                    username=employee.email,
                    email=employee.email,
                    password=make_password(password),  # Use make_password to hash the password
                    employee=employee,
                    user_type=4
                )}
            )

            if not created:
                division_head.admin.password = make_password(password)
                division_head.admin.save()

                messages.success(request, "Successfully Added/Updated Division Head Login")
            else:
                messages.success(request, "Successfully Added Division Head Login")

            # Set the division for the DivisionHead
            division_head.division = employee.division_id
            division_head.save()

            return HttpResponseRedirect(reverse("add_division_head"))

        except Exception as e:
            messages.error(request, f"Failed To Add/Update Division Head Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("add_division_head"))


# Manage division_head
def manage_division_head(request):
    division_head = DivisionHead.objects.all().order_by('-created_at')
    return render(request, "admin_template/manage_division_head_template.html", {"division_head": division_head})


# Edit division_head login
def edit_division_head(request, admin_id):
    division_head = get_object_or_404(DivisionHead, admin__id=admin_id)
    divisions = Divisions.objects.all()
    context = {
        'division_head': division_head,
        'divisions': divisions,
    }
    return render(request, "admin_template/edit_division_head_template.html", context)


def edit_division_head_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        admin_id = request.POST.get("admin_id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        division_id = request.POST.get("division")

        try:
            division_head = DivisionHead.objects.get(admin__id=admin_id)
            division_head.admin.email = email

            # Set username as email
            division_head.admin.username = email

            # Check if the password is provided for updating
            if password:
                # Validate password length
                if len(password) < 8:
                    messages.error(request, "Password must be at least 8 characters or longer.")
                    return HttpResponseRedirect(reverse("edit_division_head", args=[admin_id]))

                # Validate if password contains any whitespace
                if ' ' in password:
                    messages.error(request, "Password cannot contain any spaces.")
                    return HttpResponseRedirect(reverse("edit_division_head", args=[admin_id]))

                division_head.admin.password = make_password(password)   # make_password for hashing

            # Update the division
            division_head.division = Divisions.objects.get(division_id=division_id)

            # Save the changes
            division_head.admin.save()
            division_head.save()

            messages.success(request, "Successfully updated Division Head details")
            return HttpResponseRedirect(reverse("edit_division_head", args=[admin_id]))

        except Exception as e:
            messages.error(request, f"Failed to update Division Head details. Error: {str(e)}")
            return HttpResponseRedirect(reverse("edit_division_head", args=[admin_id]))


# Delete division_head
def delete_division_head(request, id):
    division_head = get_object_or_404(CustomUser, id=id)

    try:
        division_head.delete()
        messages.success(request, "Division Head Login Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Failed to delete Division Head Login. Error: {str(e)}")

    return HttpResponseRedirect(reverse("manage_division_head"))


# ------------------------------- DDO Login---------------------------------------
# Add DDO login
def add_ddo(request):
    employees = Employees.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, "admin_template/add_ddo_template.html", context)


def add_ddo_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        emp_id = request.POST.get("employee")
        password = request.POST.get("password")

        # Validate password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("add_ddo"))

        # Validate if password contains any whitespace
        if ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("add_ddo"))

        # Use get_object_or_404 to handle the case where the employee does not exist
        employee = get_object_or_404(Employees, emp_id=emp_id)

        try:
            # ... For ddo, user_type=5
            ddo = CustomUser.objects.create_user(username=employee.email, email=employee.email, password=password, employee=employee, user_type=5)

            ddo.save()

            messages.success(request, "Successfully Added DDO Login")
            return HttpResponseRedirect(reverse("add_ddo"))

        except Exception as e:
            messages.error(request, f"Failed To Add DDO Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("add_ddo"))


# Manage DDO
def manage_ddo(request):
    ddo = Ddo.objects.all().order_by('-created_at')
    return render(request, "admin_template/manage_ddo_template.html", {"ddo": ddo})


# Edit DDO login
def edit_ddo(request, id):
    ddo = get_object_or_404(CustomUser, id=id)
    employees = Employees.objects.all()

    context = {
        'ddo': ddo,
        'employees': employees,
    }
    return render(request, "admin_template/edit_ddo_template.html", context)


# Update email and password in the database
def edit_ddo_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        id = request.POST.get("id")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validate password length only if a new password is provided
        if password and len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("edit_ddo", args=(id,)))

        # Validate if password contains any whitespace only if a new password is provided
        if password and ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("edit_ddo", args=(id,)))

        ddo = get_object_or_404(CustomUser, id=id)

        try:
            # Update email
            ddo.email = email
            ddo.username = email  # Set username the same as email

            # Update password only if a new password is provided
            if password:
                ddo.set_password(password)

            ddo.save()

            messages.success(request, "Successfully Updated DDO Login")
            return HttpResponseRedirect(reverse("edit_ddo", args=(id,)))

        except Exception as e:
            messages.error(request, f"Failed To Update DDO Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("edit_ddo", args=(id,)))


# Delete DDO
def delete_ddo(request, id):
    ddo = get_object_or_404(CustomUser, id=id)

    try:
        ddo.delete()
        messages.success(request, "DDO Login Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Failed to delete DDO Login. Error: {str(e)}")

    return HttpResponseRedirect(reverse("manage_ddo"))


# ------------------------------- Special DG Login---------------------------------------
# Add special_dg login
def add_special_dg(request):
    employees = Employees.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, "admin_template/add_special_dg_template.html", context)


def add_special_dg_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        emp_id = request.POST.get("employee")
        password = request.POST.get("password")

        # Validate password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("add_special_dg"))

        # Validate if password contains any whitespace
        if ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("add_special_dg"))

        # Use get_object_or_404 to handle the case where the employee does not exist
        employee = get_object_or_404(Employees, emp_id=emp_id)

        try:
            # ... For special_dg, user_type=6
            special_dg = CustomUser.objects.create_user(username=employee.email, email=employee.email, password=password, employee=employee, user_type=6)

            special_dg.save()

            messages.success(request, "Successfully Added Special DG Login")
            return HttpResponseRedirect(reverse("add_special_dg"))

        except Exception as e:
            messages.error(request, f"Failed To Add Special DG Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("add_special_dg"))


# Manage Special DG
def manage_special_dg(request):
    special_dg = SpecialDg.objects.all().order_by('-created_at')
    return render(request, "admin_template/manage_special_dg_template.html", {"special_dg": special_dg})


# Edit special_dg login
def edit_special_dg(request, id):
    special_dg = get_object_or_404(CustomUser, id=id)
    employees = Employees.objects.all()

    context = {
        'special_dg': special_dg,
        'employees': employees,
    }
    return render(request, "admin_template/edit_special_dg_template.html", context)


# Update email and password in the database
def edit_special_dg_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        id = request.POST.get("id")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validate password length only if a new password is provided
        if password and len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("edit_special_dg", args=(id,)))

        # Validate if password contains any whitespace only if a new password is provided
        if password and ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("edit_special_dg", args=(id,)))

        special_dg = get_object_or_404(CustomUser, id=id)

        try:
            # Update email
            special_dg.email = email
            special_dg.username = email  # Set username the same as email

            # Update password only if a new password is provided
            if password:
                special_dg.set_password(password)

            special_dg.save()

            messages.success(request, "Successfully Updated Special DG Login")
            return HttpResponseRedirect(reverse("edit_special_dg", args=(id,)))

        except Exception as e:
            messages.error(request, f"Failed To Update Special DG Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("edit_special_dg", args=(id,)))


# Delete special_dg
def delete_special_dg(request, id):
    special_dg = get_object_or_404(CustomUser, id=id)

    try:
        special_dg.delete()
        messages.success(request, "Special DG Login Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Failed to delete Special DG Login. Error: {str(e)}")

    return HttpResponseRedirect(reverse("manage_special_dg"))


# ------------------------------- IGP Login---------------------------------------
# Add IGP login
def add_igp(request):
    employees = Employees.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, "admin_template/add_igp_template.html", context)


def add_igp_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        emp_id = request.POST.get("employee")
        password = request.POST.get("password")

        # Validate password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("add_igp"))

        # Validate if password contains any whitespace
        if ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("add_igp"))

        # Use get_object_or_404 to handle the case where the employee does not exist
        employee = get_object_or_404(Employees, emp_id=emp_id)

        try:
            # ... For igp, user_type=7
            igp = CustomUser.objects.create_user(username=employee.email, email=employee.email, password=password, employee=employee, user_type=7)

            igp.save()

            messages.success(request, "Successfully Added IGP Login")
            return HttpResponseRedirect(reverse("add_igp"))

        except Exception as e:
            messages.error(request, f"Failed To Add IGP Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("add_igp"))


# Manage IGP
def manage_igp(request):
    igp = Igp.objects.all().order_by('-created_at')
    return render(request, "admin_template/manage_igp_template.html", {"igp": igp})


# Edit igp login
def edit_igp(request, id):
    igp = get_object_or_404(CustomUser, id=id)
    employees = Employees.objects.all()

    context = {
        'igp': igp,
        'employees': employees,
    }
    return render(request, "admin_template/edit_igp_template.html", context)


# Update email and password in the database
def edit_igp_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        id = request.POST.get("id")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validate password length only if a new password is provided
        if password and len(password) < 8:
            messages.error(request, "Password must be at least 8 characters or longer.")
            return HttpResponseRedirect(reverse("edit_igp", args=(id,)))

        # Validate if password contains any whitespace only if a new password is provided
        if password and ' ' in password:
            messages.error(request, "Password cannot contain any spaces.")
            return HttpResponseRedirect(reverse("edit_igp", args=(id,)))

        igp = get_object_or_404(CustomUser, id=id)

        try:
            # Update email
            igp.email = email
            igp.username = email  # Set username the same as email

            # Update password only if a new password is provided
            if password:
                igp.set_password(password)

            igp.save()

            messages.success(request, "Successfully Updated IGP Login")
            return HttpResponseRedirect(reverse("edit_igp", args=(id,)))

        except Exception as e:
            messages.error(request, f"Failed To Update IGP Login. Error: {str(e)}")
            return HttpResponseRedirect(reverse("edit_igp", args=(id,)))


# Delete igp
def delete_igp(request, id):
    igp = get_object_or_404(CustomUser, id=id)

    try:
        igp.delete()
        messages.success(request, "IGP Login Deleted Successfully")
    except Exception as e:
        messages.error(request, f"Failed to delete IGP Login. Error: {str(e)}")

    return HttpResponseRedirect(reverse("manage_igp"))


# ------------------------------- Section---------------------------------------
# Add Section
def add_section(request):
    divisions = Divisions.objects.all()  # Fetch all divisions for the dropdown
    return render(request, "admin_template/add_section_template.html", {"divisions": divisions})


def add_section_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        # variables on right side in double quotes : name of input fields in add_employee_template.html
        # variables on the right side - should be same as defiined in models.py
        # Try to keep name of form input elements in html file and name of variables(which actually are
        # ... database columns) in models.py same.
        section_name = request.POST.get("section_name")
        description = request.POST.get("description")
        section_incharge = request.POST.get("section_incharge")
        division_id = request.POST.get("division")

        try:
            # Sections - defined in models.py
            section_model = Sections(
                section_name=section_name,
                description=description,
                section_incharge=section_incharge,
                division_id=division_id,
                )

            section_model.save()
            messages.success(request, "Successfully Added Section")
            return HttpResponseRedirect(reverse("add_section"))

        except Exception as e:
            messages.error(request, f"Failed To Add Section {str(e)}")
            return HttpResponseRedirect(reverse("add_section"))


# Manage Sections
def manage_section(request):
    # Reading all Section data by calling Sections.objects.all()
    # Sections is defined in models.py
    sections = Sections.objects.all()
    return render(request, "admin_template/manage_section_template.html", {"sections": sections})


# Edit Section
def edit_section(request, section_id):
    sections = Sections.objects.get(section_id=section_id)
    divisions = Divisions.objects.all()
    return render(request, "admin_template/edit_section_template.html", {"sections": sections, "divisions": divisions})


def edit_section_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # created a hidden input field in edit_section_template.html in the Section Name input field for Section ID
        section_id = request.POST.get("section_id")
        section_name = request.POST.get("section_name")
        description = request.POST.get("description")
        section_incharge = request.POST.get("section_incharge")
        division_id = request.POST.get("division")

        try:
            sections = Sections.objects.get(section_id=section_id)
            sections.section_name = section_name
            sections.description = description
            sections.section_incharge = section_incharge
            sections.division_id = division_id

            sections.save()
            messages.success(request, "Successfully Edited Section")
            return HttpResponseRedirect(reverse("edit_section", kwargs={"section_id": section_id}))

        except Exception as e:
            messages.error(request, f"Failed To Edit Section {str(e)}")
            return HttpResponseRedirect(reverse("edit_section", kwargs={"section_id": section_id}))


# Delete Section
def delete_section(request, section_id):
    if request.method == "POST":
        section = get_object_or_404(Sections, section_id=section_id)

        try:
            # Delete the section instance
            section.delete()
            messages.success(request, "Section and associated details deleted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete Section: {str(e)}")

        return redirect("manage_section")  # Redirect to the list of sections page


def view_all_section_details(request, section_id):
    # Fetch section details
    section = Sections.objects.get(section_id=section_id)

    # Fetch employee details for the section
    employees = Employees.objects.filter(section_id=section_id)

    return render(request, "admin_template/view_all_section_details.html", {"section": section, "employees": employees})


# ------------------------------- Employee Supervisor ---------------------------------------
# Add Employee Supervisor
def add_supervisor(request):
    # Adding sections here because it is a foreign key
    # Sections - in RHS - defined in models.py
    sections = Sections.objects.all()
    context = {
        'sections': sections,
    }
    return render(request, "admin_template/add_supervisor_template.html", context)


def add_supervisor_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        # "first_name" etc : name of input fields in add_supervisor_template.html
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        section_id = request.POST.get("section")

        # Retrieve the Sections instance using section_id
        section = Sections.objects.get(section_id=section_id)

        try:
            # Supervisor - defined in models.py
            supervisor_model = Supervisor(first_name=first_name, last_name=last_name, section_id=section)

            supervisor_model.save()

            messages.success(request, "Successfully Added Employee Supervisor")
            return HttpResponseRedirect(reverse("add_supervisor"))

        except Exception as e:
            messages.error(request, f"Failed To Add Employee Supervisor {str(e)}")
            return HttpResponseRedirect(reverse("add_supervisor"))


# Manage Supervisors
def manage_supervisor(request):
    # Reading all Employees data by calling Supervisor.objects.all()
    supervisor = Supervisor.objects.all()
    return render(request, "admin_template/manage_supervisor_template.html", {"supervisor": supervisor})


# Edit Supervisor
def edit_supervisor(request, supervisor_id):
    # Reading all Sections data using objects.all() - It is a foreign key and we need to fetch all of the data in this table.
    sections = Sections.objects.all()

    supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)

    return render(request, "admin_template/edit_supervisor_template.html",
                  {"supervisor": supervisor, "sections": sections})


def edit_supervisor_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # created a hidden input field in edit_supervisor_template.html in the First Name input field for Supervisor ID
        supervisor_id = request.POST.get("supervisor_id")

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        section_id = request.POST.get("section")

        # Retrieve the Sections instance using section_id
        section = Sections.objects.get(section_id=section_id)

        try:
            supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)

            supervisor.first_name = first_name
            supervisor.last_name = last_name
            supervisor.section_id = section  # section is defined above: section = Sections.objects.get(section_id=section_id)

            supervisor.save()

            messages.success(request, "Successfully Edited Employee Supervisor")
            return HttpResponseRedirect(reverse("edit_supervisor", kwargs={"supervisor_id": supervisor_id}))

        except Exception as e:
            messages.error(request, f"Failed To Edit Employee Supervisor {str(e)}")
            return HttpResponseRedirect(reverse("edit_supervisor", kwargs={"supervisor_id": supervisor_id}))


# Delete Employee Supervisor
def delete_supervisor(request, supervisor_id):
    if request.method == "POST":
        supervisor = get_object_or_404(Supervisor, supervisor_id=supervisor_id)

        try:
            # Delete the supervisor instance
            supervisor.delete()
            messages.success(request, "Employee Supervisor and associated details deleted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete Supervisor: {str(e)}")

        return redirect("manage_supervisor")  # Redirect to the list of Employee Supervisor page


# ------------------------------- Employee---------------------------------------
# Add Employee
def add_employee(request):
    # Adding sections, divisions and supervisor here because they are foreign keys
    # Sections and Supervisor - in RHS - defined in models.py
    sections = Sections.objects.all()
    supervisors = Supervisor.objects.all()
    divisions = Divisions.objects.all()
    ranks = Rank.objects.all()
    context = {
        'sections': sections,
        'supervisors': supervisors,
        'divisions': divisions,
        'ranks': ranks,
    }
    return render(request, "admin_template/add_employee_template.html", context)


def add_employee_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        # variables on right side in double quotes : name of input fields in add_employee_template.html
        # variables on the right side - should be same as defined in models.py
        # Try to keep name of form input elements in html file and name of variables(which actually are
        # ... database columns) in models.py same.
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # Picture automatically gets stored in the "media" folder
        # This If Else condition is used to avoid MultiValueDictKeyError which occurs if no picture is selected.
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            # Generate a unique identifier using uuid
            unique_id = str(uuid.uuid4())
            # Append the unique identifier to the original filename
            filename = f"{unique_id}_{profile_pic.name}"
            fs = FileSystemStorage()

            # profile_pic_url = fs.url(filename)  # Reading file path by url()
            # Save the file with the relative path (without 'media/') to avoid the error. Also, allows to delete the image from the'media' folder during deletion.
            profile_pic_url = fs.save(filename, profile_pic)
        else:
            profile_pic_url = None  # Set a default value if no profile pic is provided

        gender = request.POST.get("gender")
        email = request.POST.get("email")

        # Get the list of phone numbers from the form
        phone_numbers = request.POST.getlist("phone")

        address = request.POST.get("address")
        tehsil = request.POST.get("tehsil")
        district = request.POST.get("district")
        parentage = request.POST.get("parentage")
        mother_name = request.POST.get("mother_name")
        belt_no = request.POST.get("belt_no")
        pid_no = request.POST.get("pid_no")
        cpis = request.POST.get("cpis")
        date_joined = request.POST.get("date_joined")  # Date Of Joining In CID

        # Date Of Joining In CID - Document File Upload
        # Check if the document file is provided
        if 'document_file' in request.FILES:
            document_file = request.FILES['document_file']
            # Generate a unique identifier using uuid
            unique_id = str(uuid.uuid4())
            # Append the unique identifier to the original filename
            filename = f"{unique_id}_{document_file.name}"
            fs = FileSystemStorage()

            # filename = fs.save(document_file.name, document_file)
            # document_file_url = fs.url(filename)  # Reading file path by url()
            # Save the file with the relative path (without 'media/') to avoid the error. Alsp, allows to delete the doc file from the'media' folder during deletion.
            document_file_url = fs.save(filename, document_file)
        else:
            document_file_url = None  # Set a default value if no document file is provided

        date_appointment_police = request.POST.get("date_appointment_police")  # Date Of Appointment In Police
        dob = request.POST.get("dob")
        rank_id = request.POST.get("rank")
        aadhar_number = request.POST.get("aadhar_number")
        pan_number = request.POST.get("pan_number")

        # Get the list of qualifications from the form
        qualifications = request.POST.getlist("qualifications")

        # Get the list of Previous Positions Held from the form
        previous_positions_held_within_cid = request.POST.getlist("previous_positions_held_within_cid")
        previous_positions_held_outside_cid = request.POST.getlist("previous_positions_held_outside_cid")

        dialogue = request.POST.get("dialogue")
        adverse_report = request.POST.get("adverse_report")
        section_id = request.POST.get("section")
        division_id = request.POST.get("division")
        # supervisor_id = request.POST.get("supervisor")
        computer_knowledge = request.POST.get("computer_knowledge")
        computer_degree = request.POST.get("computer_degree")
        computer_skill = request.POST.get("computer_skill")
        # Get the list of Previous Positions Held from the form
        previous_trainings_done = request.POST.getlist("previous_trainings_done")
        other_emp_info = request.POST.get("other_emp_info")
        # Leave counters
        casual_leave_counter = request.POST.get("casual_leave_counter")
        earned_leave_counter = request.POST.get("earned_leave_counter")
        paternity_maternity_leave_counter = request.POST.get("paternity_maternity_leave_counter")
        committed_leave_counter = request.POST.get("committed_leave_counter")

        # Check if leave counters are empty. If they are, give them a value of 0
        if not casual_leave_counter:
            casual_leave_counter = 0
        else:
            casual_leave_counter = int(casual_leave_counter)

        # Limit casual_leave_counter to a maximum value of 20
        casual_leave_counter = min(casual_leave_counter, 20)

        if not earned_leave_counter:
            earned_leave_counter = 0
        else:
            earned_leave_counter = int(earned_leave_counter)

        if not paternity_maternity_leave_counter:
            paternity_maternity_leave_counter = 0
        else:
            paternity_maternity_leave_counter = int(paternity_maternity_leave_counter)

        if not committed_leave_counter:
            committed_leave_counter = 0
        else:
            committed_leave_counter = int(committed_leave_counter)

        # Converting date format(for date_joined). Otherwise, we'll get Invalid Date Format error.
        # change_date_format = datetime.datetime.strptime(date_joined, '%d-%m-%y').strftime('%Y-%m-%d')

        # Leaving the Date Joined input date field as empty shows an error. To fix that:
        if not date_joined:  # Check if the date_joined field is empty
            change_date_format = None  # Set to None if the field is empty
        else:
            change_date_format = datetime.datetime.strptime(date_joined, '%Y-%m-%d').date()

        if not date_appointment_police:  # Check if the date_appointment_police field is empty
            change_dap_format = None  # Set to None if the field is empty. dap : date_appointment_format
        else:
            change_dap_format = datetime.datetime.strptime(date_appointment_police, '%Y-%m-%d').date()

        if not dob:  # Check if the DOB field is empty
            change_dob_format = None  # Set to None if the field is empty
        else:
            change_dob_format = datetime.datetime.strptime(dob, '%Y-%m-%d').date()

        # Retrieve the Sections instance using section_id
        rank = Rank.objects.get(rank_id=rank_id)
        section = Sections.objects.get(section_id=section_id)
        division = Divisions.objects.get(division_id=division_id)
        # supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)

        # Check if the email, aadhar and PAN numbers are unique- email, aadhar, pan in Employees in models.py is set as unique. So, we need these validation:
        if Employees.objects.filter(email=email).exists():
            messages.error(request,
                           "There already is an existing employee with this Email. Please use your own Email ID. Also, do not keep the Email field as blank")
            return HttpResponseRedirect(reverse("add_employee"))

        # Validate Aadhar number
        if not (aadhar_number.isdigit() and len(aadhar_number) == 12):
            messages.error(request, "Aadhar Number should be a 12-digit number.")
            return HttpResponseRedirect(reverse("add_employee"))

        # Check if the aadhar number is unique
        if Employees.objects.filter(aadhar_number=aadhar_number).exists():
            messages.error(request,
                           "There already is an existing employee with this Aadhar Number. Please use your own Aadhar Number. Also, do not keep the Aadhar Number field as blank")
            return HttpResponseRedirect(reverse("add_employee"))

        # Check if the PAN number is unique
        if Employees.objects.filter(pan_number=pan_number).exists():
            messages.error(request,
                           "There already is an existing employee with this PAN Number. Please use your own PAN Number. Also, do not keep the PAN Number field as blank")
            return HttpResponseRedirect(reverse("add_employee"))

        # Check if the pid_no is unique
        if Employees.objects.filter(pid_no=pid_no).exists():
            messages.error(request,
                           "There already is an existing employee with this PID Number. Please use your own PID Number. Also, do not keep the PID Number field as blank")
            return HttpResponseRedirect(reverse("add_employee"))

        try:
            # Employees - defined in models.py. These variables are also defined in models.py. Keep LHS = RHS.
            employee_model = Employees(
                first_name=first_name,
                last_name=last_name,
                profile_pic=profile_pic_url,
                gender=gender,
                email=email,

                # Save the phone numbers as a comma-separated string in the database
                phone=",".join(phone_numbers),  # Convert the list to a string

                address=address,
                tehsil=tehsil,
                district=district,
                parentage=parentage,
                mother_name=mother_name,
                belt_no=belt_no,
                pid_no=pid_no,
                cpis=cpis,
                date_joined=change_date_format,  # Use the changed date format here
                # date_joined=date_joined,
                document_file=document_file_url,
                date_appointment_police=change_dap_format,
                dob=change_dob_format,
                rank_id=rank,  # rank is defined above: rank = Rank.objects.get(rank_id=rank_id)
                aadhar_number=aadhar_number,
                pan_number=pan_number,

                # Save the qualifications as a comma-separated string in the database
                qualifications=",".join(qualifications),  # Convert the list to a string

                # Save the Previous Positions Held as a comma-separated string in the database
                previous_positions_held_within_cid=",".join(previous_positions_held_within_cid),  # Convert the list to a string
                previous_positions_held_outside_cid=",".join(previous_positions_held_outside_cid),
                # Convert the list to a string

                dialogue=dialogue,
                adverse_report=adverse_report,
                section_id=section,  # section is defined above: section = Sections.objects.get(section_id=section_id)
                division_id=division,
                # supervisor_id=supervisor,
                # supervisor is defined above: supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
                computer_knowledge=computer_knowledge,
                computer_degree=computer_degree,
                computer_skill=computer_skill,
                # Save the previous_trainings_done as a comma-separated string in the database
                previous_trainings_done=",".join(previous_trainings_done),  # Convert the list to a string
                other_emp_info=other_emp_info,
                casual_leave_counter=casual_leave_counter,
                earned_leave_counter=earned_leave_counter,
                paternity_maternity_leave_counter=paternity_maternity_leave_counter,
                committed_leave_counter=committed_leave_counter,
            )

            employee_model.save()

            messages.success(request, "Successfully Added Employee")
            return HttpResponseRedirect(reverse("add_employee"))

        except Exception as e:
            messages.error(request, f"Failed To Add Employee: {str(e)}")
            return HttpResponseRedirect(reverse("add_employee"))


# Manage Employees
#def manage_employee(request):
    # Reading all Employees data by calling Employees.objects.all()
    #employees = Employees.objects.all()
    #return render(request, "admin_template/manage_employee_template.html", {"employees": employees})


def manage_employee(request):
    # Reading all Employees data by calling Employees.objects.all(). Order the Employees data by the date it was added.
    employee_list = Employees.objects.all().order_by('-created_at')

    # Number of employees to display per page - for Pagination
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(employee_list, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the specified page from the paginator
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        employees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results.
        employees = paginator.page(paginator.num_pages)

    return render(request, "admin_template/manage_employee_template.html", {"employees": employees})


# Edit Employees
def edit_employee(request, emp_id):
    # Reading all Supervisor, Divisions, Ranks and Sections data using objects.all() - they are foreign keys and we need to fetch all of the data in these two tables.
    sections = Sections.objects.all()
    divisions = Divisions.objects.all()
    # use 'supervisors'(not 'supervisor' or anything) because we are iterating over a variable named "supervisors" (note the plural form) to populate the dropdown list in edit_employee_template.html : ' {% for supervisor in supervisors %} '
    # supervisors = Supervisor.objects.all()
    ranks = Rank.objects.all()

    employees = Employees.objects.get(emp_id=emp_id)

    # for multiple phone numbers
    phone_numbers = employees.phone.split(",") if employees.phone else []

    # for multiple qualifications
    qualifications = employees.qualifications.split(",") if employees.qualifications else []

    # for multiple Previous Positions Held
    previous_positions_held_within_cid = employees.previous_positions_held_within_cid.split(",") if employees.previous_positions_held_within_cid else []
    previous_positions_held_outside_cid = employees.previous_positions_held_outside_cid.split(
        ",") if employees.previous_positions_held_outside_cid else []

    # for multiple previous_trainings_done
    previous_trainings_done = employees.previous_trainings_done.split(",") if employees.previous_trainings_done else []

    districts = ["Srinagar", "Baramulla", "Anantnag", "Pulwama", "Kupwara", "Shopian", "Ganderbal", "Bandipora",
                 "Budgam", "Kulgam", "Jammu", "Kathua", "Samba", "Poonch", "Rajouri", "Udhampur", "Reasi", "Ramban",
                 "Doda", "Kishtwar"]

    # return render(request, "admin_template/edit_employee_template.html",
                  #{"employees": employees, "sections": sections, "divisions": divisions, "supervisors": supervisors,
                   #"ranks": ranks, "phone_numbers": phone_numbers, "qualifications": qualifications,
                   #"previous_positions_held_within_cid": previous_positions_held_within_cid,
                   #"previous_positions_held_outside_cid": previous_positions_held_outside_cid,
                   #"previous_trainings_done": previous_trainings_done})

    return render(request, "admin_template/edit_employee_template.html",
                  {"employees": employees, "sections": sections, "divisions": divisions,
                   "ranks": ranks, "phone_numbers": phone_numbers, "qualifications": qualifications,
                   "previous_positions_held_within_cid": previous_positions_held_within_cid, "previous_positions_held_outside_cid": previous_positions_held_outside_cid, "previous_trainings_done": previous_trainings_done, 'districts': districts })


def edit_employee_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # created a hidden input field in edit_employee_template.html in the First Name input field for Employee ID
        emp_id = request.POST.get("emp_id")

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # Picture automatically gets stored in the "media" folder
        # This If Else condition is used to avoid MultiValueDictKeyError which occurs if no picture is selected.
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            # Generate a unique identifier using uuid
            unique_id = str(uuid.uuid4())
            # Append the unique identifier to the original filename
            filename = f"{unique_id}_{profile_pic.name}"
            fs = FileSystemStorage()

            # profile_pic_url = fs.url(filename)  # Reading file path by url()
            # Save the file with the relative path (without 'media/') to avoid the error. Also, allows to delete the image from the'media' folder during deletion.
            profile_pic_url = fs.save(filename, profile_pic)
        else:
            profile_pic_url = None  # Set a default value if no profile pic is provided

        gender = request.POST.get("gender")
        email = request.POST.get("email")

        # Get the list of phone numbers from the form
        phone_numbers = request.POST.getlist("phone[]")

        address = request.POST.get("address")
        tehsil = request.POST.get("tehsil")
        district = request.POST.get("district")
        parentage = request.POST.get("parentage")
        mother_name = request.POST.get("mother_name")
        belt_no = request.POST.get("belt_no")
        pid_no = request.POST.get("pid_no")
        cpis = request.POST.get("cpis")
        date_joined = request.POST.get("date_joined")  # Date Of Joining In CID

        # Date Of Joining In CID - Document File Upload
        # Check if the document file is provided
        if 'document_file' in request.FILES:
            document_file = request.FILES['document_file']
            # Generate a unique identifier using uuid
            unique_id = str(uuid.uuid4())
            # Append the unique identifier to the original filename
            filename = f"{unique_id}_{document_file.name}"
            fs = FileSystemStorage()

            # filename = fs.save(document_file.name, document_file)
            # document_file_url = fs.url(filename)  # Reading file path by url()
            # Save the file with the relative path (without 'media/') to avoid the error. Alsp, allows to delete the doc file from the'media' folder during deletion.
            document_file_url = fs.save(filename, document_file)
        else:
            document_file_url = None  # Set a default value if no document file is provided


        date_appointment_police = request.POST.get("date_appointment_police")  # Date Of Appointment In Police
        dob = request.POST.get("dob")
        rank_id = request.POST.get("rank")
        aadhar_number = request.POST.get("aadhar_number")
        pan_number = request.POST.get("pan_number")

        # Get the list of qualifications from the form
        qualifications = request.POST.getlist("qualifications[]")

        # Get the list of previous_positions_held from the form
        previous_positions_held_within_cid = request.POST.getlist("previous_positions_held_within_cid[]")
        previous_positions_held_outside_cid = request.POST.getlist("previous_positions_held_outside_cid[]")

        dialogue = request.POST.get("dialogue")
        adverse_report = request.POST.get("adverse_report")
        section_id = request.POST.get("section")
        division_id = request.POST.get("division")
        # supervisor_id = request.POST.get("supervisor")
        computer_knowledge = request.POST.get("computer_knowledge")
        computer_degree = request.POST.get("computer_degree")
        computer_skill = request.POST.get("computer_skill")
        # Get the list of previous_trainings_done from the form
        previous_trainings_done = request.POST.getlist("previous_trainings_done[]")
        other_emp_info = request.POST.get("other_emp_info")
        # Leave Counters
        casual_leave_counter = request.POST.get("casual_leave_counter")
        earned_leave_counter = request.POST.get("earned_leave_counter")
        paternity_maternity_leave_counter = request.POST.get("paternity_maternity_leave_counter")
        committed_leave_counter = request.POST.get("committed_leave_counter")

        # Check if the leave counters are empty. If they are, give them a value of 0.
        if not casual_leave_counter:
            casual_leave_counter = 0
        else:
            casual_leave_counter = int(casual_leave_counter)

        # Limit casual_leave_counter to a maximum value of 20
        casual_leave_counter = min(casual_leave_counter, 20)

        if not earned_leave_counter:
            earned_leave_counter = 0
        else:
            earned_leave_counter = int(earned_leave_counter)

        if not paternity_maternity_leave_counter:
            paternity_maternity_leave_counter = 0
        else:
            paternity_maternity_leave_counter = int(paternity_maternity_leave_counter)

        if not committed_leave_counter:
            committed_leave_counter = 0
        else:
            committed_leave_counter = int(committed_leave_counter)

        # Check if Computer Knowledge is set to "No"
        if computer_knowledge == "No":
            # Set Computer Degree and Computer Skill to "None"
            computer_degree = "None"
            computer_skill = "None"

        # Converting date format(for date_joined). Otherwise, we'll get Invalid Date Format error.
        # change_date_format = datetime.datetime.strptime(date_joined, '%d-%m-%y').strftime('%Y-%m-%d')

        # Leaving the Date Joined input date field as empty shows an error. To fix that:
        if not date_joined:  # Check if the date_joined field is empty
            change_date_format = None  # Set to None if the field is empty
        else:
            change_date_format = datetime.datetime.strptime(date_joined, '%Y-%m-%d').date()

        if not date_appointment_police:  # Check if the date_appointment_police field is empty
            change_dap_format = None  # Set to None if the field is empty. dap : date_appointment_format
        else:
            change_dap_format = datetime.datetime.strptime(date_appointment_police, '%Y-%m-%d').date()

        if not dob:  # Check if the DOB field is empty
            change_dob_format = None  # Set to None if the field is empty
        else:
            change_dob_format = datetime.datetime.strptime(dob, '%Y-%m-%d').date()

        # Retrieve the Sections instance using section_id
        section = Sections.objects.get(section_id=section_id)
        division = Divisions.objects.get(division_id=division_id)
        # supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
        rank = Rank.objects.get(rank_id=rank_id)

        # Retrieve the employee instance being edited - check- it is also written below
        # employees = Employees.objects.get(emp_id=emp_id)

        # Check if the email, aadhar and PAN numbers are unique- email, aadhar, pan in Employees in models.py is set as unique. So, we need these validation:
        # Check if the email is unique and not the same as the current employee's email.
        # If we want to edit any field and keep the email, aadhar and phone as they were, trying to edit will give error messages like "There alrady is an existing employee with this email etc." To fix it, we use 'exclude.'
        if Employees.objects.filter(email=email).exclude(emp_id=emp_id).exists():
            messages.error(request, "There already is an existing employee with this Email.")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))

        # Validate Aadhar number
        if not (aadhar_number.isdigit() and len(aadhar_number) == 12):
            messages.error(request, "Aadhar Number should be a 12-digit number.")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))

        # Check if the aadhar number is unique and not the same as the current employee's aadhar number
        if Employees.objects.filter(aadhar_number=aadhar_number).exclude(emp_id=emp_id).exists():
            messages.error(request, "There already is an existing employee with this Aadhar Number.")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))

        # Check if the PAN number is unique and not the same as the current employee's PAN number
        if Employees.objects.filter(pan_number=pan_number).exclude(emp_id=emp_id).exists():
            messages.error(request, "There already is an existing employee with this PAN Number.")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))

        # Check if the pid_no is unique and not the same as the current employee's PID number
        if Employees.objects.filter(pid_no=pid_no).exclude(emp_id=emp_id).exists():
            messages.error(request, "There already is an existing employee with this PID Number.")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))

        try:
            employees = Employees.objects.get(emp_id=emp_id)

            employees.first_name = first_name
            employees.last_name = last_name

            if profile_pic_url != None:
                employees.profile_pic = profile_pic_url

            employees.gender = gender
            employees.email = email

            # Update the phone field with a comma-separated string
            employees.phone = ",".join(phone_numbers)

            employees.address = address
            employees.tehsil = tehsil
            employees.district = district
            employees.parentage = parentage
            employees.mother_name = mother_name
            employees.belt_no = belt_no
            employees.pid_no = pid_no
            employees.cpis = cpis
            employees.date_joined = change_date_format  # Use the changed date format here
            # date_joined=date_joined,

            if document_file_url != None:
                employees.document_file = document_file_url

            employees.date_appointment_police = change_dap_format
            employees.dob = change_dob_format
            employees.rank_id = rank
            employees.aadhar_number = aadhar_number
            employees.pan_number = pan_number

            # Update the qualifications field with a comma-separated string
            employees.qualifications = ",".join(qualifications)

            # Update the previous_positions_held field with a comma-separated string
            employees.previous_positions_held_within_cid = ",".join(previous_positions_held_within_cid)
            employees.previous_positions_held_outside_cid = ",".join(previous_positions_held_outside_cid)

            employees.computer_knowledge = computer_knowledge
            employees.dialogue = dialogue
            employees.adverse_report = adverse_report
            employees.section_id = section  # section is defined above: section = Sections.objects.get(section_id=section_id)
            employees.division_id = division
            # employees.supervisor_id = supervisor
            # supervisor is defined above: supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
            employees.computer_knowledge = computer_knowledge
            employees.computer_degree = computer_degree
            employees.computer_skill = computer_skill

            # Update the previous_trainings_done field with a comma-separated string
            employees.previous_trainings_done = ",".join(previous_trainings_done)

            employees.other_emp_info = other_emp_info
            employees.casual_leave_counter = casual_leave_counter
            employees.earned_leave_counter = earned_leave_counter
            employees.paternity_maternity_leave_counter = paternity_maternity_leave_counter
            employees.committed_leave_counter = committed_leave_counter

            employees.save()

            messages.success(request, "Successfully Edited/Updated Employee")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))

        except Exception as e:
            messages.error(request, f"Failed To Edit/Update Employee {str(e)}")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))


def delete_employee(request, emp_id):
    if request.method == "POST":
        try:
            employee = Employees.objects.get(emp_id=emp_id)
        except Employees.DoesNotExist:
            raise Http404("Employee not found")

        try:
            # Get the path to the employee's profile picture
            profile_pic_path = os.path.join(settings.MEDIA_ROOT, str(employee.profile_pic))
            # Check if the profile picture file exists and is a file (not a directory)
            if os.path.isfile(profile_pic_path):
                os.remove(profile_pic_path)

            # Get the path to the Document File upload for Date of Joining In CID
            document_file_path = os.path.join(settings.MEDIA_ROOT, str(employee.document_file))
            # Check if the document_file exists and is a file (not a directory)
            if os.path.isfile(document_file_path):
                os.remove(document_file_path)

            # Delete the employee instance
            employee.delete()

            messages.success(request, "Employee and associated details deleted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete employee: {str(e)}")

        return redirect("manage_employee")  # Redirect to the list of employees page


# View all employee details
def view_all_employee(request, emp_id):
    # Fetch the specific employee using the emp_id parameter
    # get_object_or_404 : used to retrieve a single object from the database based on certain criteria, and if the object doesn't exist, it raises a Http404 exception.
    employee = get_object_or_404(Employees, emp_id=emp_id)

    #  document_file is a field in the Employees model
    doc_file = employee.document_file.url if employee.document_file else None

    context = {
        'employee': employee,
        'doc_file': doc_file,
    }
    return render(request, 'admin_template/view_all_employee_details.html', context)


# -----------------------------------------------------------
# Feedback
def user_feedback_message(request):
    # feedbacks = FeedBackUser.objects.all()
    feedbacks = FeedBackUser.objects.all().order_by('-created_at')

    # Number of entries to display per page - for Pagination
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(feedbacks, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the specified page from the paginator
        page_entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        page_entries = paginator.page(paginator.num_pages)

    return render(request, "admin_template/user_feedback_template.html", {"feedbacks": page_entries})


@csrf_exempt
def user_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackUser.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


# --------------------------------------------------------------
# Leaves
# Apply for Leaves
def admin_apply_leave(request):
    user = request.user
    employee = user.employee

    leave_data = LeaveReportEmployee.objects.all()
    ranks = Rank.objects.all()      # Check if we need this line because we're not fetching from Rank table.
    return render(request, "admin_template/admin_apply_leave.html", {"leave_data": leave_data, 'ranks': ranks, 'employee':employee})


def admin_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_apply_leave"))
    else:
        # Fetch user and employee details
        user = request.user
        employee = user.employee

        leave_start_date = request.POST.get("leave_start_date")
        leave_end_date = request.POST.get("leave_end_date")
        leave_msg = request.POST.get("leave_msg")
        leave_type = request.POST.get("leave_type")

        try:
            # Increase the respective leave counters based on the leave type
            if leave_type == 'Casual':
                # Check if the limit of 20 has been reached
                if employee.casual_leave_counter >= 20:
                    messages.error(request, "Casual leave limit reached. Cannot apply for more casual leaves.")
                    return HttpResponseRedirect(reverse("user_apply_leave"))

                employee.casual_leave_counter += 1  # Increment the counter
            elif leave_type == 'Earned':
                employee.earned_leave_counter += 1
            elif leave_type == 'Paternity/Maternity':
                employee.paternity_maternity_leave_counter += 1
            elif leave_type == 'Committed':
                employee.committed_leave_counter += 1

            # Save the changes to the employee model
            employee.save()

            # Create a new LeaveReportEmployee instance with employee details
            leave_report = LeaveReportEmployee(
                name=f"{employee.first_name} {employee.last_name}",
                pid=employee.pid_no,
                phone=employee.phone,
                rank=employee.rank_id.rank_name,
                leave_start_date=leave_start_date,
                leave_end_date=leave_end_date,
                leave_message=leave_msg,
                leave_type=leave_type,
                section=employee.section_id.section_name,
                division=employee.division_id.division_name,

                section_head_approval_status=0,
                division_head_approval_status=0,
                ddo_approval_status=0,
            )
            leave_report.save()

            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("admin_apply_leave"))
        except Exception as e:
            messages.error(request, f"Failed To Apply for Leave: {str(e)}")
            return HttpResponseRedirect(reverse("admin_apply_leave"))


# View Leave History and Status
def admin_leave_history(request):
    user = request.user
    employee = user.employee

    # Filter leave data for the current user using pid_no. Order the leave data by the date it was added.
    leave_data = LeaveReportEmployee.objects.filter(pid=request.user.employee.pid_no).order_by('-created_at')
    ranks = Rank.objects.all()

    # Number of leave entries to display per page - for Pagination
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(leave_data, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the specified page from the paginator
        leave_entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        leave_entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        leave_entries = paginator.page(paginator.num_pages)

    return render(request, "admin_template/admin_leave_history.html", {"leave_data": leave_entries, 'ranks': ranks, 'employee': employee})


# View all the department leaves
def view_all_dept_leaves(request):
    leave_data = LeaveReportEmployee.objects.all().order_by('-created_at')

    # Number of leave entries to display per page - for Pagination
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(leave_data, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the specified page from the paginator
        leave_entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        leave_entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        leave_entries = paginator.page(paginator.num_pages)

    return render(request, "admin_template/view_all_dept_leaves.html", {"leave_data": leave_entries})


# Edit the leave counters FOR ALL EMPLOYEES
def edit_leave_counters(request):
    if request.method == "POST":
        # Retrieve leave counter values from the form
        casual_leave_counter = request.POST.get("casual_leave_counter")
        earned_leave_counter = request.POST.get("earned_leave_counter")
        paternity_maternity_leave_counter = request.POST.get("paternity_maternity_leave_counter")
        committed_leave_counter = request.POST.get("committed_leave_counter")

        # Get all employees
        employees = Employees.objects.all()

        # Update leave counters for each employee individually
        for employee in employees:
            # Check if a new value is provided for each leave counter
            if casual_leave_counter is not None:
                # Update casual_leave_counter only if a new value is provided in the form
                casual_leave_value = int(casual_leave_counter) if casual_leave_counter else employee.casual_leave_counter
                casual_leave_value = min(casual_leave_value, 20)  # Limit to a maximum value of 20
                employee.casual_leave_counter = casual_leave_value

            if earned_leave_counter is not None:
                employee.earned_leave_counter = int(earned_leave_counter) if earned_leave_counter else employee.earned_leave_counter

            if paternity_maternity_leave_counter is not None:
                employee.paternity_maternity_leave_counter = int(paternity_maternity_leave_counter) if paternity_maternity_leave_counter else employee.paternity_maternity_leave_counter

            if committed_leave_counter is not None:
                employee.committed_leave_counter = int(committed_leave_counter) if committed_leave_counter else employee.committed_leave_counter

            # Save the updated employee
            employee.save()

        messages.success(request, "Leave counter updated for all employees successfully")
        return HttpResponseRedirect(reverse("edit_leave_counters"))

    return render(request, "admin_template/edit_leave_counters_template.html")


# ------------------------------- Rank---------------------------------------
# Add Ranks
def add_rank(request):
    return render(request, "admin_template/add_rank_template.html")


def add_rank_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        rank_name = request.POST.get("rank_name")
        description = request.POST.get("description")

        try:
            rank_model = Rank(rank_name=rank_name, description=description)
            rank_model.save()
            messages.success(request, "Successfully Added Rank")
            return HttpResponseRedirect(reverse("add_rank"))

        except Exception as e:
            messages.error(request, f"Failed To Add Rank {str(e)}")
            return HttpResponseRedirect(reverse("add_rank"))


# Manage Rank
def manage_rank(request):
    rank = Rank.objects.all()
    return render(request, "admin_template/manage_rank_template.html", {"rank": rank})


# Edit Rank
def edit_rank(request, rank_id):
    ranks = Rank.objects.get(rank_id=rank_id)
    return render(request, "admin_template/edit_rank_template.html", {"ranks": ranks})


def edit_rank_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # created a hidden input field in edit_rank_template.html in the Rank Name input field for Rank ID
        rank_id = request.POST.get("rank_id")
        rank_name = request.POST.get("rank_name")
        description = request.POST.get("description")

        try:
            ranks = Rank.objects.get(rank_id=rank_id)
            ranks.rank_name = rank_name
            ranks.description = description

            ranks.save()
            messages.success(request, "Successfully Edited Rank")
            return HttpResponseRedirect(reverse("edit_rank", kwargs={"rank_id": rank_id}))

        except Exception as e:
            messages.error(request, f"Failed To Edit Rank {str(e)}")
            return HttpResponseRedirect(reverse("edit_rank", kwargs={"rank_id": rank_id}))


# Delete Rank
def delete_rank(request, rank_id):
    if request.method == "POST":
        rank = get_object_or_404(Rank, rank_id=rank_id)

        try:
            # Delete the rank instance
            rank.delete()
            messages.success(request, "Rank and associated details deleted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete Rank: {str(e)}")

        return redirect("manage_rank")


def view_all_rank_details(request, rank_id):
    # Fetch rank details
    rank = Rank.objects.get(rank_id=rank_id)

    # Fetch employee details for the rank
    employees = Employees.objects.filter(rank_id=rank_id)

    return render(request, "admin_template/view_all_rank_details.html", {"rank": rank, "employees": employees})


# ------------------------------- Division---------------------------------------
# Add Division
def add_division(request):
    return render(request, "admin_template/add_division_template.html")


def add_division_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        division_name = request.POST.get("division_name")
        division_description = request.POST.get("division_description")
        division_head = request.POST.get("division_head")
        try:
            # Divisions - defined in models.py
            division_model = Divisions(division_name=division_name, division_description=division_description,
                                       division_head=division_head)
            division_model.save()

            messages.success(request, "Successfully Added Division")
            return HttpResponseRedirect(reverse("add_division"))

        except Exception as e:
            messages.error(request, f"Failed To Add Division: {str(e)}")
            return HttpResponseRedirect(reverse("add_division"))


# Manage Divisions
def manage_division(request):
    divisions = Divisions.objects.all()
    return render(request, "admin_template/manage_division_template.html", {"divisions": divisions})


"""
# Manage Divisions
def manage_division(request):
    divisions = Divisions.objects.all()

    for division in divisions:
        # Access related sections using sections_set
        division.sections = division.sections_set.all()

    return render(request, "admin_template/manage_division_template.html", {"divisions": divisions})
"""


# Edit Division
def edit_division(request, division_id):
    divisions = Divisions.objects.get(division_id=division_id)
    return render(request, "admin_template/edit_division_template.html", {"divisions": divisions})


def edit_division_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # created a hidden input field in edit_division_template.html in the Division Name input field for Division ID
        division_id = request.POST.get("division_id")
        division_name = request.POST.get("division_name")
        division_description = request.POST.get("division_description")
        division_head = request.POST.get("division_head")

        try:
            divisions = Divisions.objects.get(division_id=division_id)
            divisions.division_name = division_name
            divisions.division_description = division_description
            divisions.division_head = division_head

            divisions.save()
            messages.success(request, "Successfully Edited Division")
            return HttpResponseRedirect(reverse("edit_division", kwargs={"division_id": division_id}))

        except Exception as e:
            messages.error(request, f"Failed To Edit Division {str(e)}")
            return HttpResponseRedirect(reverse("edit_division", kwargs={"division_id": division_id}))


# Delete Division
def delete_division(request, division_id):
    if request.method == "POST":
        division = get_object_or_404(Divisions, division_id=division_id)

        try:
            # Delete the division instance
            division.delete()
            messages.success(request, "Division and associated details deleted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete Division: {str(e)}")

        return redirect("manage_division")  # Redirect to the list of divisions page


# view_all_division_details view
def view_all_division_details(request, division_id):
    # Fetch division details
    division = Divisions.objects.get(division_id=division_id)

    # Fetch employee details for the division
    employees = Employees.objects.filter(division_id=division_id)

    # Fetch sections related to the division
    sections = Sections.objects.filter(division_id=division_id)

    return render(request, "admin_template/view_all_division_details.html", {"division": division, "employees": employees, "sections": sections})


# ------------------------------- Admin Security Question (NOT BEING USED) -----------------------------
# Add admin security question
def add_admin_security_question(request):
    return render(request, "admin_template/add_admin_security_question_template.html")


def add_admin_security_question_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        id = request.POST.get("id")
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        try:
            model = AdminSecurityQuestion(id=id, question=question,
                                     answer=answer)
            model.save()
            messages.success(request, "Successfully Added Admin Security Question")
            return HttpResponseRedirect(reverse("add_admin_security_question"))

        except Exception as e:
            messages.error(request, f"Failed To Add Admin Security Question {str(e)}")
            return HttpResponseRedirect(reverse("add_admin_security_question"))


# Manage admin security question
def manage_admin_security_question(request):
    asq = AdminSecurityQuestion.objects.all()
    return render(request, "admin_template/manage_admin_security_question_template.html", {"asq": asq})


# Edit admin_security_question
def edit_admin_security_question(request, id):
    asq = AdminSecurityQuestion.objects.get(id=id)
    return render(request, "admin_template/edit_admin_security_question_template.html", {"asq": asq})


def edit_admin_security_question_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # created a hidden input field in edit_admin_security_questiontemplate.html in the Question input field for ID
        id = request.POST.get("id")
        question = request.POST.get("question")
        answer = request.POST.get("answer")

        try:
            asq = AdminSecurityQuestion.objects.get(id=id)
            asq.question = question
            asq.answer = answer

            asq.save()
            messages.success(request, "Successfully Edited Admin Security Question")
            return HttpResponseRedirect(reverse("edit_admin_security_question", kwargs={"id": id}))

        except Exception as e:
            messages.error(request, f"Failed To Edit Admin Security Question {str(e)}")
            return HttpResponseRedirect(reverse("edit_admin_security_question", kwargs={"id": id}))


# Delete admin_security_question
def delete_admin_security_question(request, id):
    if request.method == "POST":
        asq = get_object_or_404(AdminSecurityQuestion, id=id)

        try:
            asq.delete()
            messages.success(request, "Admin Security Question and associated details deleted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete Admin Security Question {str(e)}")

        return redirect("manage_admin_security_question")


# ------------------------------- User Security Question (NOT BEING USED) ------------------------
# Add user security question
def add_user_security_question(request):
    return render(request, "admin_template/add_user_security_question_template.html")


def add_user_security_question_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        id = request.POST.get("id")
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        try:
            model = UserSecurityQuestion(id=id, question=question,
                                     answer=answer)
            model.save()
            messages.success(request, "Successfully Added User Security Question")
            return HttpResponseRedirect(reverse("add_user_security_question"))

        except Exception as e:
            messages.error(request, f"Failed To Add User Security Question {str(e)}")
            return HttpResponseRedirect(reverse("add_user_security_question"))


# Manage user security question
def manage_user_security_question(request):
    usq = UserSecurityQuestion.objects.all()
    return render(request, "admin_template/manage_user_security_question_template.html", {"usq": usq})


# Edit user_security_question
def edit_user_security_question(request, id):
    usq = UserSecurityQuestion.objects.get(id=id)
    return render(request, "admin_template/edit_user_security_question_template.html", {"usq": usq})


def edit_user_security_question_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # created a hidden input field in edit_user_security_question_template.html in the Question input field for ID
        id = request.POST.get("id")
        question = request.POST.get("question")
        answer = request.POST.get("answer")

        try:
            usq = UserSecurityQuestion.objects.get(id=id)
            usq.question = question
            usq.answer = answer

            usq.save()
            messages.success(request, "Successfully Edited User Security Question")
            return HttpResponseRedirect(reverse("edit_user_security_question", kwargs={"id": id}))

        except Exception as e:
            messages.error(request, f"Failed To Edit User Security Question {str(e)}")
            return HttpResponseRedirect(reverse("edit_user_security_question", kwargs={"id": id}))


# Delete user_security_question
def delete_user_security_question(request, id):
    if request.method == "POST":
        usq = get_object_or_404(UserSecurityQuestion, id=id)

        try:
            usq.delete()
            messages.success(request, "User Security Question and associated details deleted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete User Security Question {str(e)}")

        return redirect("manage_user_security_question")


# -------------------------------------------------------
# Search
def employee_search(request):
    employees = []

    if request.method == 'POST':
        query = Employees.objects.all()

        # first_name, last_name etc is defined in employee_search.html
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        tehsil = request.POST.get('tehsil')
        district = request.POST.get('district')
        qualifications = request.POST.get('qualifications')
        section = request.POST.get('section')
        division = request.POST.get('division')
        rank = request.POST.get('rank')
        pid_no = request.POST.get('pid_no')
        cpis = request.POST.get('cpis')

        if first_name:
            query = query.filter(first_name__icontains=first_name)
        if last_name:
            query = query.filter(last_name__icontains=last_name)
        if gender:
            query = query.filter(gender__icontains=gender)
        if email:
            query = query.filter(email__icontains=email)
        if phone:
            query = query.filter(phone__icontains=phone)
        if address:
            query = query.filter(address__icontains=address)
        if tehsil:
            query = query.filter(tehsil__icontains=tehsil)
        if district:
            query = query.filter(district__icontains=district)
        if qualifications:
            query = query.filter(qualifications__icontains=qualifications)
        if section:
            query = query.filter(section_id__section_name__icontains=section)
        if division:
            query = query.filter(division_id__division_name__icontains=division)
        if rank:
            query = query.filter(rank_id__rank_name__icontains=rank)
        if pid_no:
            query = query.filter(pid_no__icontains=pid_no)
        if cpis:
            query = query.filter(cpis__icontains=cpis)

        employees = query.all()

        # Redirect to the search results page
        return render(request, 'admin_template/employee_search_results.html', {'employees': employees})

    # Render the search form on initial page load
    return render(request, 'admin_template/employee_search.html', {'employees': employees})


@login_required
def my_profile_admin(request):
    # Get the currently logged-in user
    User = get_user_model()
    user = get_object_or_404(User, username=request.user.username)

    # Redirect to the user's profile details page
    return redirect('view_all_employee', emp_id=user.employee.emp_id)


# Profile Correction Request (PCR)
def pcr_msg(request):
    pcr_msgs = ProfileCorrReq.objects.all().order_by('-created_at')

    # Number of leave entries to display per page - for Pagination
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(pcr_msgs, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the specified page from the paginator
        page_entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        page_entries = paginator.page(paginator.num_pages)

    return render(request, "admin_template/pcr_msg_template.html", {"pcr_msgs": page_entries})


@csrf_exempt
def pcr_msg_replied(request):
    id = request.POST.get("id")
    message = request.POST.get("message")

    try:
        pcr_msgs = ProfileCorrReq.objects.get(id=id)
        pcr_msgs.corr_req_reply = message
        pcr_msgs.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


# -------------------------------------
# Archive Employees
def archive_employee(request, emp_id):
    if request.method == "POST":
        try:
            employee = Employees.objects.get(emp_id=emp_id)
        except Employees.DoesNotExist:
            raise Http404("Employee not found")

        try:
            # Create an ArchivedEmployees instance and populate its fields with the employee data
            archived_employee = ArchivedEmployees(
                emp_id=employee.emp_id,
                first_name=employee.first_name,
                last_name=employee.last_name,
                profile_pic=employee.profile_pic,
                gender=employee.gender,
                email=employee.email,
                phone=employee.phone,
                address=employee.address,
                tehsil=employee.tehsil,
                district=employee.district,
                parentage=employee.parentage,
                mother_name=employee.mother_name,
                belt_no=employee.belt_no,
                pid_no=employee.pid_no,
                cpis=employee.cpis,
                date_joined=employee.date_joined,
                document_file=employee.document_file,
                date_appointment_police=employee.date_appointment_police,
                dob=employee.dob,
                rank_id=employee.rank_id,
                aadhar_number=employee.aadhar_number,
                pan_number=employee.pan_number,
                previous_positions_held_within_cid=employee.previous_positions_held_within_cid,
                previous_positions_held_outside_cid=employee.previous_positions_held_outside_cid,
                qualifications=employee.qualifications,
                dialogue=employee.dialogue,
                adverse_report=employee.adverse_report,
                section_id=employee.section_id,
                division_id=employee.division_id,
                supervisor_id=employee.supervisor_id,
                created_at=employee.created_at,
                updated_at=employee.updated_at,
                computer_knowledge=employee.computer_knowledge,
                computer_degree=employee.computer_degree,
                computer_skill=employee.computer_skill,
                previous_trainings_done=employee.previous_trainings_done,
                other_emp_info=employee.other_emp_info,
            )

            # Save the archived employee
            archived_employee.save()

            # Delete the original employee
            employee.delete()

            messages.success(request, "Employee archived successfully.")
        except Exception as e:
            messages.error(request, f"Failed to archive employee. Error: {str(e)}")

        return redirect("manage_employee")  # Redirect to the list of employees page


# Manage and view archived employees
def manage_archived_employee(request):
    # Reading all Archived Employees data by calling ArchivedEmployees.objects.all(). Order the Employees data by the date it was added.
    employee_list = ArchivedEmployees.objects.all().order_by('-archived_at')

    # Number of employees to display per page - for Pagination
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(employee_list, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the specified page from the paginator
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        employees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results.
        employees = paginator.page(paginator.num_pages)

    return render(request, "admin_template/manage_archived_employees.html", {"employees": employees})


# View all archived employee details
def view_all_archived_employee(request, emp_id):
    # Fetch the specific employee using the emp_id parameter
    employee = get_object_or_404(ArchivedEmployees, emp_id=emp_id)

    #  document_file is a field in the Employees model
    doc_file = employee.document_file.url if employee.document_file else None

    context = {
        'employee': employee,
        'doc_file': doc_file,
    }
    return render(request, 'admin_template/view_all_employee_details.html', context)


def delete_archived_employee(request, emp_id):
    if request.method == "POST":
        try:
            employee = ArchivedEmployees.objects.get(emp_id=emp_id)
        except ArchivedEmployees.DoesNotExist:
            raise Http404("Archived Employee not found")

        try:
            # Get the path to the archived employee's profile picture
            profile_pic_path = os.path.join(settings.MEDIA_ROOT, str(employee.profile_pic))
            # Check if the profile picture file exists and is a file (not a directory)
            if os.path.isfile(profile_pic_path):
                os.remove(profile_pic_path)

            # Get the path to the Document File upload for Date of Joining In CID
            document_file_path = os.path.join(settings.MEDIA_ROOT, str(employee.document_file))
            # Check if the document_file exists and is a file (not a directory)
            if os.path.isfile(document_file_path):
                os.remove(document_file_path)

            # Delete the archived employee instance
            employee.delete()

            messages.success(request, "Employee and associated details deleted from the Archive Folder successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete employee from the Archive Folder. Error: {str(e)}")

        return redirect("manage_archived_employee")  # Redirect to the list of archived employees page