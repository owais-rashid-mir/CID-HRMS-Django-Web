import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from hrms_cid_app.models import CustomUser, User, Sections, Supervisor, Employees


def admin_home(request):
    return render(request, "admin_template/home_content.html")


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

            # Data only getting stored in customuser table. Fix it. Above, we are passing data to customuser table only
            # user.user.address = address
            user.save()
            messages.success(request, "Successfully Added User Login")
            return HttpResponseRedirect(reverse("add_user"))  # Once data is added, return to add_user page.
        except:
            messages.error(request, "Failed to Add User Login")
            return HttpResponseRedirect(reverse("add_user"))


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


def add_supervisor(request):
    return render(request, "admin_template/add_supervisor_template.html")


def add_supervisor_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        # "first_name" etc : name of input fields in add_supervisor_template.html
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        try:
            # Supervisor - defined in models.py
            supervisor_model = Supervisor(first_name=first_name, last_name=last_name)
            supervisor_model.save()
            messages.success(request, "Successfully Added Section")
            return HttpResponseRedirect(reverse("add_supervisor"))
        except:
            messages.error(request, "Failed To Add Section")
            return HttpResponseRedirect(reverse("add_supervisor"))


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
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        date_joined = request.POST.get("date_joined")
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
        # change_date_format = datetime.datetime.strptime(date_joined, '%Y-%m-%d').date()


        # Retrieve the Sections instance using section_id
        section = Sections.objects.get(section_id=section_id)
        supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)

        # Check if the email, aadhar and PAN numbers are unique- email, aadhar, pan in Employees in models.py is set as unique. So, we need these validation:
        if Employees.objects.filter(email=email).exists():
            messages.error(request, "There already is an existing employee with this Email. Please use your own Email ID. Also, do not keep the Email field as blank")
            return HttpResponseRedirect(reverse("add_employee"))

        # Check if the aadhar number is unique
        if Employees.objects.filter(aadhar_number=aadhar_number).exists():
            messages.error(request, "There already is an existing employee with this Aadhar Number. Please use your own Aadhar Number. Also, do not keep the Aadhar Number field as blank")
            return HttpResponseRedirect(reverse("add_employee"))

        # Check if the PAN number is unique
        if Employees.objects.filter(pan_number=pan_number).exists():
            messages.error(request, "There already is an existing employee with this PAN Number. Please use your own PAN Number. Also, do not keep the PAN Number field as blank")
            return HttpResponseRedirect(reverse("add_employee"))

        try:
            # Employees - defined in models.py. These variables are also defined in models.py. Keep LHS = RHS.
            employee_model = Employees(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                email=email,
                phone=phone,
                address=address,
                # date_joined=change_date_format,     # Use the changed date format here
                date_joined=date_joined,
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
