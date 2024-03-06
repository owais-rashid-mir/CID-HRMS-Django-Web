from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hrms_cid_app.models import LeaveReportEmployee, Employees, FeedBackUser, Divisions, Sections, Rank, ProfileCorrReq
from django.db.models import Q


@login_required
def special_dg_home(request):
    employee_count = Employees.objects.all().count()
    division_count = Divisions.objects.all().count()
    section_count = Sections.objects.all().count()
    rank_count = Rank.objects.all().count()

    # Special DG is logged in, redirect to the special_dg home page
    return render(request, "special_dg_template/special_dg_home_template.html",
                      {"employee_count": employee_count, "division_count": division_count, "section_count": section_count,
                       "rank_count": rank_count})


# Manage Leaves - Special DG
def manage_leaves_sp_dg(request):
    # Define gazetted ranks
    gazetted_ranks = [
        'DySP', 'SP', 'SSP', 'Senior PO', 'CPO', 'DDP', 'DIG', 'IGP', 'ADGP', 'Special DG'
    ]

    # Filter leaves for Special DG based on gazetted ranks and specific leave types
    """
    for special dg, these leaves are visible:
    1) if rank is gazetted and type of leave is earned, paternity/maternity or committed.
    2) if rank is SSP(for DivHead and DDO) and type of leave  is casual, earned, paternity/maternity or committed(all 4 types of leaves).
    """
    leaves = LeaveReportEmployee.objects.filter(
        Q(rank__in=gazetted_ranks, leave_type__in=['Earned', 'Paternity/Maternity', 'Committed']) |
        Q(rank='SSP', leave_type__in=['Casual', 'Earned', 'Paternity/Maternity', 'Committed'])
    ).order_by('-created_at')

    # Number of leave entries to display per page - for Pagination
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(leaves, items_per_page)

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

    return render(request, "special_dg_template/manage_leaves_sp_dg.html", {"leaves": page_entries})


# Approve/Disapprove Leaves
def approve_leave_sp_dg(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    # Check if the rank is "SSP" (Division Head and DDO), allow approval without Division Head and IGP checks
    if leave.rank == 'SSP':
        if leave.leave_type == 'Casual':
            # Increment the casual leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.casual_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Casual Leave Approved by Special DG. Casual leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment casual leave counter. Error: {str(e)}")
        elif leave.leave_type == 'Earned':
            # Increment the earned leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.earned_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Earned Leave Approved by Special DG. Earned leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment earned leave counter. Error: {str(e)}")
        elif leave.leave_type == 'Paternity/Maternity':
            # Increment the paternity/maternity leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.paternity_maternity_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Paternity/Maternity Leave Approved by Special DG. Paternity/Maternity leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment paternity/maternity leave counter. Error: {str(e)}")
        elif leave.leave_type == 'Committed':
            # Increment the committed leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.committed_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request,
                                 "Committed Leave Approved by Special DG. Committed leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment committed leave counter. Error: {str(e)}")
        else:
            messages.warning(request, "Leave type not eligible for Special DG approval")

        return HttpResponseRedirect(reverse("manage_leaves_sp_dg"))

    # 0: Pending,   1: Approved,   and 2: Disapproved.
    if (
        leave.division_head_approval_status == 1
        and leave.igp_approval_status == 1
        and leave.special_dg_approval_status == 0
    ):
        # Check leave type and rank before approval
        gazetted_ranks = [
            'DySP', 'SP', 'SSP', 'Senior PO', 'CPO', 'DDP', 'DIG', 'IGP', 'ADGP', 'Special DG'
        ]

        if leave.leave_type == 'Casual' and leave.rank in gazetted_ranks:
            messages.warning(request, "Casual leaves do not require Special DG approval/disapproval")
        elif leave.leave_type == 'Earned' and leave.rank in gazetted_ranks:
            # Increment the earned leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.earned_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Earned Leave Approved by Special DG. Earned leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment earned leave counter. Error: {str(e)}")
        elif leave.leave_type == 'Paternity/Maternity' and leave.rank in gazetted_ranks:
            # Increment the paternity/maternity leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.paternity_maternity_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Paternity/Maternity Leave Approved by Special DG. Paternity/Maternity leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment paternity/maternity leave counter. Error: {str(e)}")
        elif leave.leave_type == 'Committed' and leave.rank in gazetted_ranks:
            # Increment the committed leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.committed_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Committed Leave Approved by Special DG. Committed leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment committed leave counter. Error: {str(e)}")
        else:
            messages.warning(request, "Leave type or rank not eligible for Special DG approval")
    else:
        messages.warning(request, "Leave has not been approved by Division Head, IGP, or already processed by Special DG.")

    return HttpResponseRedirect(reverse("manage_leaves_sp_dg"))


def disapprove_leave_sp_dg(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    # Check if the rank is "SSP" (Division Head and DDO), allow disapproval without Division Head and IGP checks
    if leave.rank == 'SSP':
        leave.special_dg_approval_status = 2
        leave.save()
        messages.success(request, "Leave Disapproved by Special DG.")
        return HttpResponseRedirect(reverse("manage_leaves_sp_dg"))

    if (
        leave.division_head_approval_status == 1
        and leave.igp_approval_status == 1
        and leave.special_dg_approval_status == 0
    ):

        gazetted_ranks = [
            'DySP', 'SP', 'SSP', 'Senior PO', 'CPO', 'DDP', 'DIG', 'IGP', 'ADGP', 'Special DG'
        ]

        if leave.leave_type == 'Casual' and leave.rank in gazetted_ranks:
            messages.warning(request, "Casual leaves do not require Special DG approval/disapproval")
            return HttpResponseRedirect(reverse("manage_leaves_sp_dg"))
        else:
            leave.special_dg_approval_status = 2
            leave.save()
            messages.success(request, "Leave Disapproved by Special DG.")
    else:
        messages.warning(request, "Leave has not been approved by Division Head or IGP.")

    return HttpResponseRedirect(reverse("manage_leaves_sp_dg"))


# Override Approve and Disapprove leaves - Even if Division Head or IGP have not approved a leave, the Special DG can bypass or override the restrictions, and directly approve or disapprove the leave.
def override_approve_leave_sp_dg(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    # 0: Pending,   1: Approved,   and 2: Disapproved.
    if leave.special_dg_approval_status == 0:
        # Check leave type and rank before approval
        gazetted_ranks = [
            'DySP', 'SP', 'SSP', 'Senior PO', 'CPO', 'DDP', 'DIG', 'IGP', 'ADGP', 'Special DG'
        ]

        if leave.leave_type == 'Casual' and leave.rank in gazetted_ranks:
            # Increment the casual leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.casual_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Casual Leave Approved by Special DG. Casual leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment casual leave counter. Error: {str(e)}")
        elif leave.leave_type == 'Earned' and leave.rank in gazetted_ranks:
            # Increment the earned leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.earned_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Earned Leave Approved by Special DG. Earned leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment earned leave counter. Error: {str(e)}")
        elif leave.leave_type == 'Paternity/Maternity' and leave.rank in gazetted_ranks:
            # Increment the paternity/maternity leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.paternity_maternity_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Paternity/Maternity Leave Approved by Special DG. Paternity/Maternity leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment paternity/maternity leave counter. Error: {str(e)}")
        elif leave.leave_type == 'Committed' and leave.rank in gazetted_ranks:
            # Increment the committed leave counter
            try:
                employee = Employees.objects.get(pid_no=leave.pid)
                employee.committed_leave_counter += 1
                employee.save()
                leave.special_dg_approval_status = 1
                leave.save()
                messages.success(request, "Committed Leave Approved by Special DG. Committed leave counter incremented.")
            except Employees.DoesNotExist:
                messages.error(request, "Employee not found")
            except Exception as e:
                messages.error(request, f"Failed to increment committed leave counter. Error: {str(e)}")
        else:
            messages.warning(request, "Leave type not eligible for Special DG approval")
    else:
        messages.warning(request, "Leave has not been approved by Division Head, IGP, or already processed by Special DG.")

    return HttpResponseRedirect(reverse("manage_leaves_sp_dg"))


def override_disapprove_leave_sp_dg(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)

    if leave.special_dg_approval_status == 0:

        gazetted_ranks = [
            'DySP', 'SP', 'SSP', 'Senior PO', 'CPO', 'DDP', 'DIG', 'IGP', 'ADGP', 'Special DG'
        ]

        if leave.leave_type == 'Casual' and leave.rank in gazetted_ranks:
            messages.warning(request, "Casual leaves do not require Special DG approval/disapproval")
            return HttpResponseRedirect(reverse("manage_leaves_sp_dg"))
        else:
            leave.special_dg_approval_status = 2
            leave.save()
            messages.success(request, "Leave Disapproved by Special DG.")
    else:
        messages.warning(request, "Leave has not been approved by Division Head or IGP.")

    return HttpResponseRedirect(reverse("manage_leaves_sp_dg"))


# NOT BEING USED - SHORTCUTS REMOVED BUT BACKEND CODE IS KEPT - BECAUSE Special DG leaves are applied offline.
# Apply for Leaves - Special DG
def sp_dg_apply_leave(request):
    user = request.user
    employee = user.employee

    leave_data = LeaveReportEmployee.objects.all()
    ranks = Rank.objects.all()      # Check if we need this line because we're not fetching from Rank table.
    return render(request, "special_dg_template/sp_dg_apply_leave.html", {"leave_data": leave_data, 'ranks': ranks, 'employee':employee})


def sp_dg_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("sp_dg_apply_leave"))
    else:
        # Fetch user and employee details
        user = request.user
        employee = user.employee

        leave_start_date = request.POST.get("leave_start_date")
        leave_end_date = request.POST.get("leave_end_date")
        leave_msg = request.POST.get("leave_msg")
        leave_type = request.POST.get("leave_type")

        try:
            if leave_type == 'Casual':
                # Check if the limit of 20 has been reached
                if employee.casual_leave_counter >= 20:
                    messages.error(request, "Casual leave limit reached. Cannot apply for more casual leaves.")
                    return HttpResponseRedirect(reverse("sp_dg_apply_leave"))

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
            return HttpResponseRedirect(reverse("sp_dg_apply_leave"))
        except Exception as e:
            messages.error(request, f"Failed To Apply for Leave: {str(e)}")
            return HttpResponseRedirect(reverse("sp_dg_apply_leave"))


# View Leave History and Status
def sp_dg_leave_history(request):
    user = request.user
    employee = user.employee

    # Filter leave data for the current user using pid_no. Order by recent date
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

    return render(request, "special_dg_template/sp_dg_leave_history.html", {"leave_data": page_entries, 'ranks': ranks, 'employee': employee})


# View all employee details - for My Profile
def view_all_employee_sp_dg(request, emp_id):
    # Fetch the specific employee using the emp_id parameter
    # get_object_or_404 : used to retrieve a single object from the database based on certain criteria, and if the object doesn't exist, it raises a Http404 exception.
    employee = get_object_or_404(Employees, emp_id=emp_id)

    #  document_file is a field in the Employees model
    doc_file = employee.document_file.url if employee.document_file else None

    context = {
        'employee': employee,
        'doc_file': doc_file,
    }
    return render(request, 'special_dg_template/view_all_employee_details_sp_dg.html', context)


@login_required
def my_profile_sp_dg(request):
    # Get the currently logged-in user
    User = get_user_model()
    user = get_object_or_404(User, username=request.user.username)

    # Redirect to the user's profile details page
    return redirect('view_all_employee_sp_dg', emp_id=user.employee.emp_id)


# -------------------------------------------------------------------------------------
# Feedback
def sp_dg_feedback(request):
    user = request.user
    employee = user.employee

    feedback_data = FeedBackUser.objects.all()
    return render(request, "special_dg_template/sp_dg_feedback.html", {"feedback_data": feedback_data, 'employee': employee})


def sp_dg_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("sp_dg_feedback_save"))
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
            return HttpResponseRedirect(reverse("sp_dg_feedback"))

        except Exception as e:
            messages.error(request, f"Failed To Send Feedback or Report a Problem. Error: {str(e)}")
            return HttpResponseRedirect(reverse("sp_dg_feedback"))


# View Feedback/Report a Problem status & history
def sp_dg_feedback_history(request):
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

    return render(request, "special_dg_template/sp_dg_feedback_history.html", {"feedback_data": page_entries})


# -------------------------------------------------------------------------------------
# Profile Correction Request
def profile_corr_req_sp_dg(request):
    user = request.user
    employee = user.employee

    corr_req_data = ProfileCorrReq.objects.all()

    return render(request, "special_dg_template/profile_corr_req_sp_dg.html",
                  {"corr_req_data": corr_req_data, 'employee': employee})


def profile_corr_req_sp_dg_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("profile_corr_req_sp_dg_save"))
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
            return HttpResponseRedirect(reverse("profile_corr_req_sp_dg"))

        except Exception as e:
            messages.error(request, f"Failed To Send Profile Correction Request. Error: {str(e)}")
            return HttpResponseRedirect(reverse("profile_corr_req_sp_dg"))


# View Profile Correction Request Message History & Status
def profile_corr_req_sp_dg_history(request):
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

    return render(request, "special_dg_template/profile_corr_req_history.html", {"corr_req_data": page_entries})

# -------------------------------------------------------------------------------------
