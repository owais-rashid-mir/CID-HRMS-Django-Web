from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from hrms_cid_app.models import LeaveReportEmployee, Employees, FeedBackUser, Divisions, Sections, Rank, ProfileCorrReq


# User homepage - redirect to user_home_template.html
def user_home(request):
    return render(request, "user_template/user_home_template.html")


# -------------------------------------------------------------------------------------
# Apply for Leaves
def user_apply_leave(request):
    user = request.user
    employee = user.employee

    leave_data = LeaveReportEmployee.objects.all()
    ranks = Rank.objects.all()  # Check if we need this line because we're not fetching from Rank table.
    return render(request, "user_template/user_apply_leave.html",
                  {"leave_data": leave_data, 'ranks': ranks, 'employee': employee})


def user_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("user_apply_leave"))
    else:
        # Fetch user and employee details
        user = request.user
        employee = user.employee

        leave_start_date = request.POST.get("leave_start_date")
        leave_end_date = request.POST.get("leave_end_date")
        leave_msg = request.POST.get("leave_msg")
        leave_type = request.POST.get("leave_type")

        try:
            '''
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
            '''

            if leave_type == 'Casual':
                # Check if the limit of 20 has been reached
                if employee.casual_leave_counter >= 20:
                    messages.error(request, "Casual leave limit reached. Cannot apply for more casual leaves.")
                    return HttpResponseRedirect(reverse("user_apply_leave"))

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
            return HttpResponseRedirect(reverse("user_apply_leave"))
        except Exception as e:
            messages.error(request, f"Failed To Apply for Leave. Error: {str(e)}")
            return HttpResponseRedirect(reverse("user_apply_leave"))


# View Leave History and Status
def user_leave_history(request):
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
        page_entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        page_entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        page_entries = paginator.page(paginator.num_pages)

    return render(request, "user_template/user_leave_history.html", {"leave_data": page_entries, 'ranks': ranks, 'employee': employee})


# -------------------------------------------------------------------------------------
# Feedback
def user_feedback(request):
    user = request.user
    employee = user.employee

    feedback_data = FeedBackUser.objects.all()
    return render(request, "user_template/user_feedback.html", {"feedback_data": feedback_data, 'employee': employee})


def user_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("user_feedback_save"))
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
            return HttpResponseRedirect(reverse("user_feedback"))

        except Exception as e:
            messages.error(request, f"Failed To Send Feedback or Report a Problem. Error: {str(e)}")
            return HttpResponseRedirect(reverse("user_feedback"))


# View Feedback/Report a Problem status & history
def user_feedback_history(request):
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

    return render(request, "user_template/user_feedback_history.html", {"feedback_data": page_entries})


# -------------------------------------------------------------------------------------
# View all employee details - for My Profile
def view_all_employee_user(request, emp_id):
    # Fetch the specific employee using the emp_id parameter
    employee = get_object_or_404(Employees, emp_id=emp_id)

    #  document_file is a field in the Employees model
    doc_file = employee.document_file.url if employee.document_file else None

    context = {
        'employee': employee,
        'doc_file': doc_file,
    }
    return render(request, 'user_template/view_all_employee_details_user.html', context)


@login_required
def my_profile_user(request):
    # Get the currently logged-in user
    User = get_user_model()
    user = get_object_or_404(User, username=request.user.username)

    # Redirect to the user's profile details page
    return redirect('view_all_employee_user', emp_id=user.employee.emp_id)


# -------------------------------------------------------------------------------------
# Profile Correction Request
def profile_corr_req_user(request):
    user = request.user
    employee = user.employee

    corr_req_data = ProfileCorrReq.objects.all()

    return render(request, "user_template/profile_corr_req_user.html",
                  {"corr_req_data": corr_req_data, 'employee': employee})


def profile_corr_req_user_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("profile_corr_req_user_save"))
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
            return HttpResponseRedirect(reverse("profile_corr_req_user"))

        except Exception as e:
            messages.error(request, f"Failed To Send Profile Correction Request. Error: {str(e)}")
            return HttpResponseRedirect(reverse("profile_corr_req_user"))


# View Profile Correction Request Message History & Status
def profile_corr_req_user_history(request):
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

    return render(request, "user_template/profile_corr_req_history.html", {"corr_req_data": page_entries})

# -------------------------------------------------------------------------------------
