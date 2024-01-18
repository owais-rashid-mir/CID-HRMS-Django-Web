from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hrms_cid_app.models import LeaveReportEmployee, Employees, FeedBackUser, Divisions, Sections, Rank, SectionHead, \
    ProfileCorrReq


@login_required
def section_head_home(request):
    employee_count = Employees.objects.all().count()
    division_count = Divisions.objects.all().count()
    section_count = Sections.objects.all().count()
    rank_count = Rank.objects.all().count()

    # Section Head is logged in, redirect to the Section Head home page
    return render(request, "section_head_template/section_head_home_template.html",
                      {"employee_count": employee_count, "division_count": division_count, "section_count": section_count,
                       "rank_count": rank_count})


# Manage Leaves - Approve/Disapprove
def manage_leaves_sh(request):
    try:
        # Get the Section Head object
        section_head = SectionHead.objects.get(admin=request.user)

        # Check if the section_head is not None
        if section_head:
            # Filter section_leaves based on non-gazetted ranks and the section name of the logged-in Section Head
            non_gazetted_ranks = ['SPO', 'Follower', 'Constable', 'SGCT', 'HC', 'ASI', 'SI', 'Inspector']

            section_leaves = LeaveReportEmployee.objects.filter(
                rank__in=non_gazetted_ranks,
                section=section_head.section.section_name  # Extract the section name
            ).order_by('-created_at')

            # ---- Pagination starts
            # Number of leave entries to display per page - for Pagination
            items_per_page = 10

            # Create a Paginator object
            paginator = Paginator(section_leaves, items_per_page)

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

            # --- Pagination Ends.

            return render(request, "section_head_template/manage_leaves_sh.html", {"leaves": page_entries})
        else:
            # Handle the case where section_head is None
            return render(request, "section_head_template/manage_leaves_sh.html", {"leaves": []})
    except SectionHead.DoesNotExist:
        # Handle the case where the SectionHead object does not exist for the current user
        return render(request, "section_head_template/manage_leaves_sh.html", {"leaves": []})


# Approve Leave - Section Head
def approve_leave_sh(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    if leave.section_head_approval_status == 0:

        # Check leave type and rank before approval
        if leave.leave_type == 'Casual' and leave.rank in ['SPO', 'Follower', 'Constable', 'SGCT', 'HC', 'ASI', 'SI', 'Inspector']:
            leave.section_head_approval_status = 1
            leave.save()
            messages.success(request, "Leave Approved by Section Head. Forwarded to Division Head.")

        elif leave.leave_type in ['Earned', 'Paternity/Maternity', 'Committed'] and leave.rank in ['SPO', 'Follower', 'Constable', 'SGCT', 'HC', 'ASI', 'SI', 'Inspector']:
            leave.section_head_approval_status = 1
            leave.save()
            messages.success(request, "Leave Approved by Section Head. Forwarded to Division Head.")

        else:
            messages.warning(request, "Leave type or rank not eligible for Section Head approval")

    else:
        messages.warning(request, "Leave has already been processed by Section Head")

    return HttpResponseRedirect(reverse("manage_leaves_sh"))


def disapprove_leave_sh(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    if leave.section_head_approval_status == 0:
        leave.section_head_approval_status = 2
        leave.save()
        messages.success(request, "Leave Disapproved by Section Head")
    else:
        messages.warning(request, "Leave has already been processed by Section Head")

    return HttpResponseRedirect(reverse("manage_leaves_sh"))


# Apply for Leaves
def sh_apply_leave(request):
    user = request.user
    employee = user.employee

    leave_data = LeaveReportEmployee.objects.all()
    ranks = Rank.objects.all()      # Check if we need this line because we're not fetching from Rank table.
    return render(request, "section_head_template/sh_apply_leave.html", {"leave_data": leave_data, 'ranks': ranks, 'employee':employee})


def sh_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("sh_apply_leave"))
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
            return HttpResponseRedirect(reverse("sh_apply_leave"))
        except Exception as e:
            messages.error(request, f"Failed To Apply for Leave: {str(e)}")
            return HttpResponseRedirect(reverse("sh_apply_leave"))


# View Leave History and Status
def sh_leave_history(request):
    user = request.user
    employee = user.employee

    # Filter leave data for the current user using pid_no.
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
        page_entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        page_entries = paginator.page(paginator.num_pages)

    return render(request, "section_head_template/sh_leave_history.html", {"leave_data": page_entries, 'ranks': ranks, 'employee': employee})


# View all employee details - for My Profile
def view_all_employee_sh(request, emp_id):
    # Fetch the specific employee using the emp_id parameter
    # get_object_or_404 : used to retrieve a single object from the database based on certain criteria, and if the object doesn't exist, it raises a Http404 exception.
    employee = get_object_or_404(Employees, emp_id=emp_id)

    #  document_file is a field in the Employees model
    doc_file = employee.document_file.url if employee.document_file else None

    context = {
        'employee': employee,
        'doc_file': doc_file,
    }
    return render(request, 'section_head_template/view_all_employee_details_sh.html', context)


@login_required
def my_profile_sh(request):
    # Get the currently logged-in user
    User = get_user_model()
    user = get_object_or_404(User, username=request.user.username)

    # Redirect to the user's profile details page
    return redirect('view_all_employee_sh', emp_id=user.employee.emp_id)


# view_all_section_details_sh - For My Section
def view_all_section_details_sh(request, section_id):
    # Fetch section details
    section = Sections.objects.get(section_id=section_id)

    # Fetch employee details for the section
    employees = Employees.objects.filter(section_id=section_id)

    return render(request, "section_head_template/view_all_section_details_sh.html", {"section": section, "employees": employees})


@login_required
def my_section_sh(request):
    # Get the currently logged-in user
    User = get_user_model()
    user = get_object_or_404(User, username=request.user.username)

    # Check if the user has a SectionHead instance
    try:
        section_head = SectionHead.objects.get(admin=user)
    except SectionHead.DoesNotExist:
        # Redirect to a different page or show an error message for non-Section Heads
        return redirect('section_head_home')  # Update with the appropriate URL for non-Section Heads

    # Redirect to the Section Head's section details page
    return redirect('view_all_section_details_sh', section_id=section_head.section.section_id)


# -------------------------------------------------------------------------------------
# Feedback
def sh_feedback(request):
    user = request.user
    employee = user.employee

    feedback_data = FeedBackUser.objects.all()
    return render(request, "section_head_template/sh_feedback.html", {"feedback_data": feedback_data, 'employee': employee})


def sh_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("sh_feedback_save"))
    else:
        # Fetch user and employee details
        user = request.user
        employee = user.employee

        feedback_msg = request.POST.get("feedback_msg")

        try:
            feedback = FeedBackUser(
                name=f"{employee.first_name} {employee.last_name}",
                pid=employee.pid_no,
                phone=employee.phone,
                rank=employee.rank_id.rank_name,
                section=employee.section_id.section_name,
                division=employee.division_id.division_name,
                feedback=feedback_msg,
                feedback_reply="",
            )

            feedback.save()

            messages.success(request, "Successfully Sent Feedback/Reported a Problem")
            return HttpResponseRedirect(reverse("sh_feedback"))

        except Exception as e:
            messages.error(request, f"Failed To Send Feedback or Report a Problem. Error: {str(e)}")
            return HttpResponseRedirect(reverse("sh_feedback"))


# View Feedback/Report a Problem status & history
def sh_feedback_history(request):
    # Filter PCR data for the current user using pid_no.
    feedback_data = FeedBackUser.objects.filter(pid=request.user.employee.pid_no).order_by('-created_at')

    # Number of leave entries to display per page - for Pagination
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(feedback_data, items_per_page)

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

    return render(request, "section_head_template/sh_feedback_history.html", {"feedback_data": page_entries})


# -------------------------------------------------------------------------------------
# Profile Correction Request
def profile_corr_req_sh(request):
    user = request.user
    employee = user.employee

    corr_req_data = ProfileCorrReq.objects.all()

    return render(request, "section_head_template/profile_corr_req_sh.html",
                  {"corr_req_data": corr_req_data, 'employee': employee})


def profile_corr_req_sh_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("profile_corr_req_sh_save"))
    else:
        # Fetch user and employee details
        user = request.user
        employee = user.employee

        corr_req_msg = request.POST.get("corr_req_msg")

        try:
            corr_req = ProfileCorrReq(
                name=f"{employee.first_name} {employee.last_name}",
                pid=employee.pid_no,
                phone=employee.phone,
                rank=employee.rank_id.rank_name,
                section=employee.section_id.section_name,
                division=employee.division_id.division_name,
                corr_req_msg=corr_req_msg,
                corr_req_reply="",
            )

            corr_req.save()

            messages.success(request, "Successfully Sent Profile Correction Request")
            return HttpResponseRedirect(reverse("profile_corr_req_sh"))

        except Exception as e:
            messages.error(request, f"Failed To Send Profile Correction Request. Error: {str(e)}")
            return HttpResponseRedirect(reverse("profile_corr_req_sh"))


# View Profile Correction Request Message History & Status
def profile_corr_req_sh_history(request):
    # Filter PCR data for the current user using pid_no.
    corr_req_data = ProfileCorrReq.objects.filter(pid=request.user.employee.pid_no).order_by('-created_at')

    # Number of leave entries to display per page - for Pagination
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(corr_req_data, items_per_page)

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

    return render(request, "section_head_template/profile_corr_req_history.html", {"corr_req_data": page_entries})

# -------------------------------------------------------------------------------------
