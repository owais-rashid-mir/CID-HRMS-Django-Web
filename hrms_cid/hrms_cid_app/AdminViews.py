# Contains the logic for Admin-side functionality and features.

import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from hrms_cid_app.models import CustomUser, User, Sections, Supervisor, Employees


def admin_home(request):
    return render(request, "admin_template/home_content.html")


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

        except:
            messages.error(request, "Failed to Add User Login. Try using another Email and Username.")
            return HttpResponseRedirect(reverse("add_user"))


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
        except:
            messages.error(request, "Failed To Add Section")
            return HttpResponseRedirect(reverse("add_section"))


# Add Supervisor
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
            # section_id=section- section is defined above: section = Sections.objects.get(section_id=section_id)
            supervisor_model = Supervisor(first_name=first_name, last_name=last_name, section_id=section)

            supervisor_model.save()

            messages.success(request, "Successfully Added Section")
            return HttpResponseRedirect(reverse("add_supervisor"))
        except:
            messages.error(request, "Failed To Add Section")
            return HttpResponseRedirect(reverse("add_supervisor"))


# Add Employee
def add_employee(request):
    # Adding sections and supervisor here because they are foreign keys
    # Sections and Supervisor - in RHS - defined in models.py
    sections = Sections.objects.all()
    supervisors = Supervisor.objects.all()
    context = {
        'sections': sections,
        'supervisors': supervisors,
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
            profile_pic_url = fs.url(filename)  # Reading file path by url()
        else:
            profile_pic_url = None  # Set a default value if no profile pic is provided

        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        date_joined = request.POST.get("date_joined")
        dob = request.POST.get("dob")
        position = request.POST.get("position")
        aadhar_number = request.POST.get("aadhar_number")
        pan_number = request.POST.get("pan_number")
        previous_positions_held = request.POST.get("previous_positions_held")
        qualifications = request.POST.get("qualifications")
        computer_knowledge = request.POST.get("computer_knowledge")
        dialogue = request.POST.get("dialogue")
        adverse_report = request.POST.get("adverse_report")
        section_id = request.POST.get("section")
        supervisor_id = request.POST.get("supervisor")

        # Converting date format(for date_joined). Otherwise, we'll get Invalid Date Format error.
        # change_date_format = datetime.datetime.strptime(date_joined, '%d-%m-%y').strftime('%Y-%m-%d')

        # Leaving the Date Joined input date field as empty shows an error. To fix that:
        if not date_joined:  # Check if the date_joined field is empty
            change_date_format = None  # Set to None if the field is empty
        else:
            change_date_format = datetime.datetime.strptime(date_joined, '%Y-%m-%d').date()

        if not dob:  # Check if the DOB field is empty
            change_dob_format = None  # Set to None if the field is empty
        else:
            change_dob_format = datetime.datetime.strptime(dob, '%Y-%m-%d').date()

        # Retrieve the Sections instance using section_id
        section = Sections.objects.get(section_id=section_id)
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
                phone=phone,
                address=address,
                date_joined=change_date_format,  # Use the changed date format here
                # date_joined=date_joined,
                dob=change_dob_format,
                position=position,
                aadhar_number=aadhar_number,
                pan_number=pan_number,
                previous_positions_held=previous_positions_held,
                qualifications=qualifications,
                computer_knowledge=computer_knowledge,
                dialogue=dialogue,
                adverse_report=adverse_report,
                section_id=section,  # section is defined above: section = Sections.objects.get(section_id=section_id)
                supervisor_id=supervisor,
                # supervisor is defined above: supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
            )

            employee_model.save()

            messages.success(request, "Successfully Added Employee")
            return HttpResponseRedirect(reverse("add_employee"))

        except:
            messages.error(request, "Failed To Add Employee")
            return HttpResponseRedirect(reverse("add_employee"))


# Manage Sections
def manage_section(request):
    # Reading all Section data by calling Sections.objects.all()
    # Sections is defined in models.py
    sections = Sections.objects.all()
    return render(request, "admin_template/manage_section_template.html", {"sections": sections})


# Manage Sections
def manage_employee(request):
    # Reading all Employees data by calling Employees.objects.all()
    employees = Employees.objects.all()
    return render(request, "admin_template/manage_employee_template.html", {"employees": employees})


# Manage Supervisors
def manage_supervisor(request):
    # Reading all Employees data by calling Supervisor.objects.all()
    supervisor = Supervisor.objects.all()
    return render(request, "admin_template/manage_supervisor_template.html", {"supervisor": supervisor})


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
        except:
            messages.error(request, "Failed to Edit User. Try using another Email and Username.")
            return HttpResponseRedirect(reverse("edit_user", kwargs={"staff_id": id}))


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
        except:
            messages.error(request, "Failed to Edit Section")
            return HttpResponseRedirect(reverse("edit_section", kwargs={"section_id": section_id}))


# Edit Employees
def edit_employee(request, emp_id):
    # Reading all Supervisor and Sections data using objects.all() - they are foreign keys and we need to fetch all of the data in these two tables.
    sections = Sections.objects.all()
    # use 'supervisors'(not 'supervisor' or anything) because we are iterating over a variable named "supervisors" (note the plural form) to populate the dropdown list in edit_employee_template.html : ' {% for supervisor in supervisors %} '
    supervisors = Supervisor.objects.all()

    employees = Employees.objects.get(emp_id=emp_id)
    return render(request, "admin_template/edit_employee_template.html",
                  {"employees": employees, "sections": sections, "supervisors": supervisors})


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
            profile_pic_url = fs.url(filename)  # Reading file path by url()
        else:
            profile_pic_url = None  # Set a default value if no profile pic is provided

        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        date_joined = request.POST.get("date_joined")
        dob = request.POST.get("dob")
        position = request.POST.get("position")
        aadhar_number = request.POST.get("aadhar_number")
        pan_number = request.POST.get("pan_number")
        previous_positions_held = request.POST.get("previous_positions_held")
        qualifications = request.POST.get("qualifications")
        computer_knowledge = request.POST.get("computer_knowledge")
        dialogue = request.POST.get("dialogue")
        adverse_report = request.POST.get("adverse_report")
        section_id = request.POST.get("section")
        supervisor_id = request.POST.get("supervisor")

        # Converting date format(for date_joined). Otherwise, we'll get Invalid Date Format error.
        # change_date_format = datetime.datetime.strptime(date_joined, '%d-%m-%y').strftime('%Y-%m-%d')

        # Leaving the Date Joined input date field as empty shows an error. To fix that:
        if not date_joined:  # Check if the date_joined field is empty
            change_date_format = None  # Set to None if the field is empty
        else:
            change_date_format = datetime.datetime.strptime(date_joined, '%Y-%m-%d').date()

        if not dob:  # Check if the DOB field is empty
            change_dob_format = None  # Set to None if the field is empty
        else:
            change_dob_format = datetime.datetime.strptime(dob, '%Y-%m-%d').date()

        # Retrieve the Sections instance using section_id
        section = Sections.objects.get(section_id=section_id)
        supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)

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
            employees.phone = phone
            employees.address = address
            employees.date_joined = change_date_format  # Use the changed date format here
            # date_joined=date_joined,
            employees.dob = change_dob_format
            employees.position = position
            employees.aadhar_number = aadhar_number
            employees.pan_number = pan_number
            employees.previous_positions_held = previous_positions_held
            employees.qualifications = qualifications
            employees.computer_knowledge = computer_knowledge
            employees.dialogue = dialogue
            employees.adverse_report = adverse_report
            employees.section_id = section  # section is defined above: section = Sections.objects.get(section_id=section_id)
            employees.supervisor_id = supervisor
            # supervisor is defined above: supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)

            employees.save()

            messages.success(request, "Successfully Edited Employee")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))
        except:
            messages.error(request, "Failed to Edit Employee")
            return HttpResponseRedirect(reverse("edit_employee", kwargs={"emp_id": emp_id}))


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

            messages.success(request, "Successfully Edited Supervisor")
            return HttpResponseRedirect(reverse("edit_supervisor", kwargs={"supervisor_id": supervisor_id}))
        except:
            messages.error(request, "Failed to Edit Supervisor")
            return HttpResponseRedirect(reverse("edit_supervisor", kwargs={"supervisor_id": supervisor_id}))


# View all employee details
def view_all_employee(request, emp_id):
    # Fetch the specific employee using the emp_id parameter
    # get_object_or_404 : used to retrieve a single object from the database based on certain criteria, and if the object doesn't exist, it raises a Http404 exception.
    employee = get_object_or_404(Employees, emp_id=emp_id)
    context = {'employee': employee}
    return render(request, 'admin_template/view_all_employee_details.html', context)

