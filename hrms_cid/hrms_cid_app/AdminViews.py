# Contains the logic for Admin-side functionality and features.

import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import logging

from hrms_cid_app.models import CustomUser, User, Sections, Supervisor, Employees, FeedBackUser, LeaveReportEmployee, \
    Rank, Divisions, AdminSecurityQuestion, UserSecurityQuestion


def admin_home(request):
    # For fetching the count on Admin homepage(home_content.html)
    employee_count = Employees.objects.all().count()
    division_count = Divisions.objects.all().count()
    section_count = Sections.objects.all().count()
    rank_count = Rank.objects.all().count()

    return render(request, "admin_template/home_content.html",{"employee_count":employee_count,"division_count":division_count, "section_count":section_count,"rank_count":rank_count} )


# Add user login
def add_user(request):
    return render(request, "admin_template/add_user_template.html")


# Taking FORM data from add_user_template.html, processing it, and storing it in our database.
def add_user_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        # first_name is the name of form input field in add_user_template.html
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # CustomUser is defined in models.py.
            # Giving this user some admin access. Storing in CustomUser table which has the login
            # ... credentials of Admin as well as User. For Admin, user_type=1   .
            # ... For User, user_type=2
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name, first_name=first_name, user_type=2)

            user.save()
            messages.success(request, "Successfully Added User Login")
            return HttpResponseRedirect(reverse("add_user"))  # Once data is added, return to add_user page.

        except Exception as e:
            messages.error(request, f"Failed To Add User Login. Try using another Email and Username. {str(e)}")
            return HttpResponseRedirect(reverse("add_user"))


# ------------------------------- Section---------------------------------------
# Add Section
def add_section(request):
    return render(request, "admin_template/add_section_template.html")


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
        try:
            # Sections - defined in models.py
            section_model = Sections(section_name=section_name, description=description,
                                     section_incharge=section_incharge)
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
    return render(request, "admin_template/edit_section_template.html", {"sections": sections})


def edit_section_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # created a hidden input field in edit_section_template.html in the Section Name input field for Section ID
        section_id = request.POST.get("section_id")
        section_name = request.POST.get("section_name")
        description = request.POST.get("description")
        section_incharge = request.POST.get("section_incharge")

        try:
            sections = Sections.objects.get(section_id=section_id)
            sections.section_name = section_name
            sections.description = description
            sections.section_incharge = section_incharge

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
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            # profile_pic_url = fs.url(filename)  # Reading file path by url()
            # Save the file with the relative path (without 'media/') to avoid the error. Also, allows to delete the image from the'media' folder during deletion.
            profile_pic_url = profile_pic.name
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
        date_joined = request.POST.get("date_joined")  # Date Of Joining In CID

        # Date Of Joining In CID - Document File Upload
        # Check if the document file is provided
        if 'document_file' in request.FILES:
            document_file = request.FILES['document_file']
            fs = FileSystemStorage()
            filename = fs.save(document_file.name, document_file)
            # document_file_url = fs.url(filename)  # Reading file path by url()
            # Save the file with the relative path (without 'media/') to avoid the error. Alsp, allows to delete the doc file from the'media' folder during deletion.
            document_file_url = document_file.name
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
        supervisor_id = request.POST.get("supervisor")
        computer_knowledge = request.POST.get("computer_knowledge")
        computer_degree = request.POST.get("computer_degree")
        computer_skill = request.POST.get("computer_skill")

        # Get the list of Previous Positions Held from the form
        previous_trainings_done = request.POST.getlist("previous_trainings_done")

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
        supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)

        # Check if the email, aadhar and PAN numbers are unique- email, aadhar, pan in Employees in models.py is set as unique. So, we need these validation:
        if Employees.objects.filter(email=email).exists():
            messages.error(request,
                           "There already is an existing employee with this Email. Please use your own Email ID. Also, do not keep the Email field as blank")
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
                supervisor_id=supervisor,
                # supervisor is defined above: supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
                computer_knowledge=computer_knowledge,
                computer_degree=computer_degree,
                computer_skill=computer_skill,
                # Save the previous_trainings_done as a comma-separated string in the database
                previous_trainings_done=",".join(previous_trainings_done),  # Convert the list to a string
            )

            employee_model.save()

            messages.success(request, "Successfully Added Employee")
            return HttpResponseRedirect(reverse("add_employee"))

        except Exception as e:
            messages.error(request, f"Failed To Add Employee: {str(e)}")
            return HttpResponseRedirect(reverse("add_employee"))


# Manage Employees
def manage_employee(request):
    # Reading all Employees data by calling Employees.objects.all()
    employees = Employees.objects.all()
    return render(request, "admin_template/manage_employee_template.html", {"employees": employees})


# Edit Employees
def edit_employee(request, emp_id):
    # Reading all Supervisor, Divisions, Ranks and Sections data using objects.all() - they are foreign keys and we need to fetch all of the data in these two tables.
    sections = Sections.objects.all()
    divisions = Divisions.objects.all()
    # use 'supervisors'(not 'supervisor' or anything) because we are iterating over a variable named "supervisors" (note the plural form) to populate the dropdown list in edit_employee_template.html : ' {% for supervisor in supervisors %} '
    supervisors = Supervisor.objects.all()
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

    return render(request, "admin_template/edit_employee_template.html",
                  {"employees": employees, "sections": sections, "supervisors": supervisors, "divisions": divisions,
                   "ranks": ranks, "phone_numbers": phone_numbers, "qualifications": qualifications,
                   "previous_positions_held_within_cid": previous_positions_held_within_cid, "previous_positions_held_outside_cid": previous_positions_held_outside_cid, "previous_trainings_done": previous_trainings_done })


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
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            # profile_pic_url = fs.url(filename)  # Reading file path by url()
            # Save the file with the relative path (without 'media/') to avoid the error. Alsp, allows to delete the image file from the'media' folder during deletion.
            profile_pic_url = profile_pic.name
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
        date_joined = request.POST.get("date_joined")  # Date Of Joining In CID

        # Date Of Joining In CID - Document File Upload
        # Check if the document file is provided
        if 'document_file' in request.FILES:
            document_file = request.FILES['document_file']
            fs = FileSystemStorage()
            filename = fs.save(document_file.name, document_file)
            # document_file_url = fs.url(filename)  # Reading file path by url()
            # Save the file with the relative path (without 'media/') to avoid the error. Alsp, allows to delete the doc file from the'media' folder during deletion.
            document_file_url = document_file.name
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
        supervisor_id = request.POST.get("supervisor")
        computer_knowledge = request.POST.get("computer_knowledge")
        computer_degree = request.POST.get("computer_degree")
        computer_skill = request.POST.get("computer_skill")

        # Get the list of previous_trainings_done from the form
        previous_trainings_done = request.POST.getlist("previous_trainings_done[]")

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
        supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
        rank = Rank.objects.get(rank_id=rank_id)

        # Retrieve the employee instance being edited - check- it is also written below
        # employees = Employees.objects.get(emp_id=emp_id)

        # Check if the email, aadhar and PAN numbers are unique- email, aadhar, pan in Employees in models.py is set as unique. So, we need these validation:
        # Check if the email is unique and not the same as the current employee's email.
        # If we want to edit any field and keep the email, aadhar and phone as they were, trying to edit will give error messages like "There alrady is an existing employee with this email etc." To fix it, we use 'exclude.'
        if Employees.objects.filter(email=email).exclude(emp_id=emp_id).exists():
            messages.error(request, "There already is an existing employee with this Email.")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))

        # Check if the aadhar number is unique and not the same as the current employee's aadhar number
        if Employees.objects.filter(aadhar_number=aadhar_number).exclude(emp_id=emp_id).exists():
            messages.error(request, "There already is an existing employee with this Aadhar Number.")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))

        # Check if the PAN number is unique and not the same as the current employee's PAN number
        if Employees.objects.filter(pan_number=pan_number).exclude(emp_id=emp_id).exists():
            messages.error(request, "There already is an existing employee with this PAN Number.")
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
            employees.supervisor_id = supervisor
            # supervisor is defined above: supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
            employees.computer_knowledge = computer_knowledge
            employees.computer_degree = computer_degree
            employees.computer_skill = computer_skill

            # Update the previous_trainings_done field with a comma-separated string
            employees.previous_trainings_done = ",".join(previous_trainings_done)

            employees.save()

            messages.success(request, "Successfully Edited Employee")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))

        except Exception as e:
            messages.error(request, f"Failed To Edit Employee {str(e)}")
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


# Manage Users
def manage_user(request):
    # Reading all User data by calling user.objects.all()
    user = User.objects.all()
    return render(request, "admin_template/manage_user_template.html", {"user": user})


# Edit Users
def edit_user(request, id):  # id of User table
    # id at the right is the id column of User table. admin is defined in the User class in models.py
    user = User.objects.get(admin=id)
    return render(request, "admin_template/edit_user_template.html", {"user": user, "id": id})


def edit_user_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        id = request.POST.get("id")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")

        try:
            user = CustomUser.objects.get(id=id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            user_model = User.objects.get(admin=id)
            user_model.save()
            messages.success(request, "Successfully Edited User")
            return HttpResponseRedirect(reverse("edit_user", kwargs={"id": id}))

        except Exception as e:
            messages.error(request, f"Failed To Edit User. Try using another Email and Username. {str(e)}")
            return HttpResponseRedirect(reverse("edit_user", kwargs={"staff_id": id}))


# Feedback
def user_feedback_message(request):
    feedbacks = FeedBackUser.objects.all()
    return render(request, "admin_template/user_feedback_template.html", {"feedbacks": feedbacks})


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


# Leaves
def user_leave_view(request):
    leaves = LeaveReportEmployee.objects.all()
    return render(request, "admin_template/user_leave_view.html", {"leaves": leaves})


def user_approve_leave(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("user_leave_view"))


def user_disapprove_leave(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("user_leave_view"))


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


# ------------------------------- Admin Security Question---------------------------------------
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


# ------------------------------- User Security Question---------------------------------------
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