from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hrms_cid_app.models import LeaveReportEmployee, Employees, FeedBackUser, Divisions, Sections, Rank, DivisionHead, \
    ProfileCorrReq


@login_required
def division_head_home(request):
    employee_count = Employees.objects.all().count()
    division_count = Divisions.objects.all().count()
    section_count = Sections.objects.all().count()
    rank_count = Rank.objects.all().count()

    # Division Head is logged in, redirect to the Division Head home page
    return render(request, "division_head_template/division_head_home_template.html",
                      {"employee_count": employee_count, "division_count": division_count, "section_count": section_count,
                       "rank_count": rank_count})


# Manage leaves
def manage_leaves_dh(request):
    try:
        # Get the Section Head object
        division_head = DivisionHead.objects.get(admin=request.user)

        # Check if the division_head is not None
        if division_head:
            # Filter division_leaves based on the division name of the logged-in Division Head
            division_leaves = LeaveReportEmployee.objects.filter(
                division=division_head.division.division_name  # Extract the division name
            ).order_by('-created_at')

            # --- Pagination starts
            # Number of leave entries to display per page - for Pagination
            items_per_page = 10

            # Create a Paginator object
            paginator = Paginator(division_leaves, items_per_page)

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

            # --- Pagination Ends

            return render(request, "division_head_template/manage_leaves_dh.html", {"leaves": page_entries})
        else:
            # Handle the case where division_head is None
            return render(request, "division_head_template/manage_leaves_dh.html", {"leaves": []})
    except DivisionHead.DoesNotExist:
        # Handle the case where the DivisionHead object does not exist for the current user
        return render(request, "division_head_template/manage_leaves_dh.html", {"leaves": []})


# Approve/Disapprove leaves
def approve_leave_dh(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    gazetted_ranks = [
        'DySP', 'SP', 'SSP', 'Senior PO', 'CPO', 'DDP', 'DIG', 'IGP', 'ADGP', 'Special DG'
    ]

    non_gazetted_ranks = [
        'SPO', 'Follower', 'Constable', 'SGCT', 'HC', 'ASI', 'SI', 'Inspector'
    ]

    # 0: Pending,   1: Approved,   and 2: Disapproved.
    # Check if Division Head Approval Status is pending.
    if leave.division_head_approval_status == 0:

        # Check leave type and rank before approval
        if leave.leave_type == 'Casual' and leave.rank in non_gazetted_ranks:
            # Non-gazetted officers with Casual leave require Section Head approval
            if leave.section_head_approval_status == 1:
                leave.division_head_approval_status = 1
                leave.save()
                messages.success(request, "Leave Approved by Division Head")
            else:
                messages.warning(request, "Leave has not been approved by Section Head")

        elif leave.leave_type in ['Earned', 'Paternity/Maternity', 'Committed'] and leave.rank in non_gazetted_ranks:
            # Non-gazetted officers with other leave types also require Section Head and Division Head approval
            if leave.section_head_approval_status == 1:
                leave.division_head_approval_status = 1
                leave.save()
                messages.success(request, "Leave Approved by Division Head. Forwarded to DDO.")
            else:
                messages.warning(request, "Leave has not been approved by Section Head")

        elif leave.leave_type == 'Casual' and leave.rank in gazetted_ranks:
            # Gazetted officers with Casual leave require only Division Head approval
            leave.division_head_approval_status = 1
            leave.save()
            messages.success(request, "Leave Approved by Division Head")

        elif leave.leave_type in ['Earned', 'Paternity/Maternity', 'Committed'] and leave.rank in gazetted_ranks:
            # Gazetted officers with these leaves require  Division Head, IGP and Special DG approval
            leave.division_head_approval_status = 1
            leave.save()
            messages.success(request, "Leave Approved by Division Head. Forwarded to IGP.")
        else:
            messages.warning(request, "Leave type or rank not eligible for Division Head approval")
    else:
        messages.warning(request, "Leave has already been processed by Division Head")

    return HttpResponseRedirect(reverse("manage_leaves_dh"))


def disapprove_leave_dh(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    gazetted_ranks = [
        'DySP', 'SP', 'SSP', 'Senior PO', 'CPO', 'DDP', 'DIG', 'IGP', 'ADGP', 'Special DG'
    ]

    non_gazetted_ranks = [
        'SPO', 'Follower', 'Constable', 'SGCT', 'HC', 'ASI', 'SI', 'Inspector'
    ]

    # Check if Division Head has Not Approved (0) the leave
    if leave.division_head_approval_status == 0:

        # Check leave type and rank before disapproval
        if leave.leave_type == 'Casual' and leave.rank in non_gazetted_ranks:
            # Non-gazetted officers with Casual leave require Section Head approval
            if leave.section_head_approval_status == 1:
                leave.division_head_approval_status = 2  # Mark as disapproved
                leave.save()
                messages.success(request, "Leave Disapproved by Division Head")
            else:
                messages.warning(request, "Leave has not been approved by Section Head")

        elif leave.leave_type in ['Earned', 'Paternity/Maternity', 'Committed'] and leave.rank in non_gazetted_ranks:
            # Non-gazetted officers with other leave types also require Section Head and Division Head approval
            if leave.section_head_approval_status == 1:
                leave.division_head_approval_status = 2  # Mark as disapproved
                leave.save()
                messages.success(request, "Leave Disapproved by Division Head")
            else:
                messages.warning(request, "Leave has not been approved by Section Head")

        elif leave.leave_type == 'Casual' and leave.rank in gazetted_ranks:
            # Gazetted officers with Casual leave require only Division Head approval
            leave.division_head_approval_status = 2  # Mark as disapproved
            leave.save()
            messages.success(request, "Leave Disapproved by Division Head")

        elif leave.leave_type in ['Earned', 'Paternity/Maternity', 'Committed'] and leave.rank in gazetted_ranks:
            leave.division_head_approval_status = 2  # Mark as disapproved
            leave.save()
            messages.success(request, "Leave Disapproved by Division Head")
        else:
            messages.warning(request, "Leave type or rank not eligible for Division Head disapproval")
    else:
        messages.warning(request, "Leave has already been processed by Division Head")

    return HttpResponseRedirect(reverse("manage_leaves_dh"))


# Override Approve and Disapprove leaves - Even if Section Head has not a leave, the Division Head can bypass or override the restrictions, and directly approve or disapprove the leave.
def override_approve_leave_dh(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    gazetted_ranks = [
        'DySP', 'SP', 'SSP', 'Senior PO', 'CPO', 'DDP', 'DIG', 'IGP', 'ADGP', 'Special DG'
    ]

    non_gazetted_ranks = [
        'SPO', 'Follower', 'Constable', 'SGCT', 'HC', 'ASI', 'SI', 'Inspector'
    ]

    # 0: Pending,   1: Approved,   and 2: Disapproved.
    # Check if Division Head Approval Status is pending.
    if leave.division_head_approval_status == 0:

        # Check leave type and rank before approval
        if leave.leave_type == 'Casual' and leave.rank in non_gazetted_ranks:
            # Non-gazetted officers with Casual leave require Section Head approval
            if leave.division_head_approval_status == 0:
                leave.division_head_approval_status = 1
                leave.save()
                messages.success(request, "Leave Approved by Division Head")
            else:
                messages.warning(request, "Leave has not been approved by Section Head")

        elif leave.leave_type in ['Earned', 'Paternity/Maternity', 'Committed'] and leave.rank in non_gazetted_ranks:
            # Non-gazetted officers with other leave types also require Section Head and Division Head approval
            if leave.division_head_approval_status == 0:
                leave.division_head_approval_status = 1
                leave.save()
                messages.success(request, "Leave Approved by Division Head. Forwarded to DDO.")
            else:
                messages.warning(request, "Leave has not been approved by Section Head")

        elif leave.leave_type == 'Casual' and leave.rank in gazetted_ranks:
            # Gazetted officers with Casual leave require only Division Head approval
            leave.division_head_approval_status = 1
            leave.save()
            messages.success(request, "Leave Approved by Division Head")

        elif leave.leave_type in ['Earned', 'Paternity/Maternity', 'Committed'] and leave.rank in gazetted_ranks:
            # Gazetted officers with these leaves require  Division Head, IGP and Special DG approval
            leave.division_head_approval_status = 1
            leave.save()
            messages.success(request, "Leave Approved by Division Head. Forwarded to IGP.")
        else:
            messages.warning(request, "Leave type or rank not eligible for Division Head approval")
    else:
        messages.warning(request, "Leave has already been processed by Division Head")

    return HttpResponseRedirect(reverse("manage_leaves_dh"))


def override_disapprove_leave_dh(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    gazetted_ranks = [
        'DySP', 'SP', 'SSP', 'Senior PO', 'CPO', 'DDP', 'DIG', 'IGP', 'ADGP', 'Special DG'
    ]

    non_gazetted_ranks = [
        'SPO', 'Follower', 'Constable', 'SGCT', 'HC', 'ASI', 'SI', 'Inspector'
    ]

    # Check if Division Head has Not Approved (0) the leave
    if leave.division_head_approval_status == 0:

        # Check leave type and rank before disapproval
        if leave.leave_type == 'Casual' and leave.rank in non_gazetted_ranks:
            # Non-gazetted officers with Casual leave require Section Head approval
            if leave.division_head_approval_status == 0:
                leave.division_head_approval_status = 2  # Mark as disapproved
                leave.save()
                messages.success(request, "Leave Disapproved by Division Head")
            else:
                messages.warning(request, "Leave has not been approved by Section Head")

        elif leave.leave_type in ['Earned', 'Paternity/Maternity', 'Committed'] and leave.rank in non_gazetted_ranks:
            # Non-gazetted officers with other leave types also require Section Head and Division Head approval
            if leave.division_head_approval_status == 0:
                leave.division_head_approval_status = 2  # Mark as disapproved
                leave.save()
                messages.success(request, "Leave Disapproved by Division Head")
            else:
                messages.warning(request, "Leave has not been approved by Section Head")

        elif leave.leave_type == 'Casual' and leave.rank in gazetted_ranks:
            # Gazetted officers with Casual leave require only Division Head approval
            leave.division_head_approval_status = 2  # Mark as disapproved
            leave.save()
            messages.success(request, "Leave Disapproved by Division Head")

        elif leave.leave_type in ['Earned', 'Paternity/Maternity', 'Committed'] and leave.rank in gazetted_ranks:
            leave.division_head_approval_status = 2  # Mark as disapproved
            leave.save()
            messages.success(request, "Leave Disapproved by Division Head")
        else:
            messages.warning(request, "Leave type or rank not eligible for Division Head disapproval")
    else:
        messages.warning(request, "Leave has already been processed by Division Head")

    return HttpResponseRedirect(reverse("manage_leaves_dh"))


# Apply for Leaves
def dh_apply_leave(request):
    user = request.user
    employee = user.employee

    leave_data = LeaveReportEmployee.objects.all()
    ranks = Rank.objects.all()      # Check if we need this line because we're not fetching from Rank table.
    return render(request, "division_head_template/dh_apply_leave.html", {"leave_data": leave_data, 'ranks': ranks, 'employee':employee})


def dh_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("dh_apply_leave"))
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
            return HttpResponseRedirect(reverse("dh_apply_leave"))
        except Exception as e:
            messages.error(request, f"Failed To Apply for Leave: {str(e)}")
            return HttpResponseRedirect(reverse("dh_apply_leave"))


# View Leave History and Status
def dh_leave_history(request):
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

    return render(request, "division_head_template/dh_leave_history.html", {"leave_data": page_entries, 'ranks': ranks, 'employee': employee})


# View all employee details - for My Profile
def view_all_employee_dh(request, emp_id):
    # Fetch the specific employee using the emp_id parameter
    # get_object_or_404 : used to retrieve a single object from the database based on certain criteria, and if the object doesn't exist, it raises a Http404 exception.
    employee = get_object_or_404(Employees, emp_id=emp_id)

    #  document_file is a field in the Employees model
    doc_file = employee.document_file.url if employee.document_file else None

    context = {
        'employee': employee,
        'doc_file': doc_file,
    }
    return render(request, 'division_head_template/view_all_employee_details_dh.html', context)


@login_required
def my_profile_dh(request):
    # Get the currently logged-in user
    User = get_user_model()
    user = get_object_or_404(User, username=request.user.username)

    # Redirect to the user's profile details page
    return redirect('view_all_employee_dh', emp_id=user.employee.emp_id)


# view_all_division_details_dh - For My Division
def view_all_division_details_dh(request, division_id):
    # Fetch division details
    division = Divisions.objects.get(division_id=division_id)

    # Fetch employee details for the division
    employees = Employees.objects.filter(division_id=division_id)

    # Fetch sections related to the division
    sections = Sections.objects.filter(division_id=division_id)

    return render(request, "division_head_template/view_all_division_details_dh.html", {"division": division, "employees": employees, "sections": sections})


@login_required
def my_division_dh(request):
    # Get the currently logged-in user
    User = get_user_model()
    user = get_object_or_404(User, username=request.user.username)

    # Check if the user has a SectionHead instance
    try:
        division_head = DivisionHead.objects.get(admin=user)
    except DivisionHead.DoesNotExist:
        # Redirect to a different page or show an error message for non-Division Heads
        return redirect('division_head_home')

    # Redirect to the Division Head's division details page
    return redirect('view_all_division_details_dh', division_id=division_head.division.division_id)


# -------------------------------------------------------------------------------------
# Feedback
def dh_feedback(request):
    user = request.user
    employee = user.employee

    feedback_data = FeedBackUser.objects.all()
    return render(request, "division_head_template/dh_feedback.html", {"feedback_data": feedback_data, 'employee': employee})


def dh_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("dh_feedback_save"))
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
            return HttpResponseRedirect(reverse("dh_feedback"))

        except Exception as e:
            messages.error(request, f"Failed To Send Feedback or Report a Problem. Error: {str(e)}")
            return HttpResponseRedirect(reverse("dh_feedback"))


# View Feedback/Report a Problem status & history
def dh_feedback_history(request):
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

    return render(request, "division_head_template/dh_feedback_history.html", {"feedback_data": page_entries})


# -------------------------------------------------------------------------------------
# Profile Correction Request
def profile_corr_req_dh(request):
    user = request.user
    employee = user.employee

    corr_req_data = ProfileCorrReq.objects.all()

    return render(request, "division_head_template/profile_corr_req_dh.html",
                  {"corr_req_data": corr_req_data, 'employee': employee})


def profile_corr_req_dh_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("profile_corr_req_dh_save"))
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
            return HttpResponseRedirect(reverse("profile_corr_req_dh"))

        except Exception as e:
            messages.error(request, f"Failed To Send Profile Correction Request. Error: {str(e)}")
            return HttpResponseRedirect(reverse("profile_corr_req_dh"))


# View Profile Correction Request Message History & Status
def profile_corr_req_dh_history(request):
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

    return render(request, "division_head_template/profile_corr_req_history.html", {"corr_req_data": page_entries})

# -------------------------------------------------------------------------------------

