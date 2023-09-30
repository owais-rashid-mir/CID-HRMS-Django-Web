from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from hrms_cid_app.models import LeaveReportEmployee, Employees, FeedBackUser


def user_home(request):
    return render(request, "user_template/user_home_template.html")


# Apply for Leaves
def user_apply_leave(request):
    # emp_obj = Employees.objects.get(request.Employees.emp_id)
    # Retrieve all leave application records - change it later. We want it for particular ID only(check)
    leave_data = LeaveReportEmployee.objects.all()
    return render(request, "user_template/user_apply_leave.html", {"leave_data": leave_data})


def user_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("user_apply_leave"))
    else:
        name = request.POST.get("name")
        leave_start_date = request.POST.get("leave_start_date")
        leave_end_date = request.POST.get("leave_end_date")
        leave_msg = request.POST.get("leave_msg")

        try:
            leave_report = LeaveReportEmployee(name=name, leave_start_date=leave_start_date, leave_end_date=leave_end_date, leave_message=leave_msg,
                                               leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("user_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("user_apply_leave"))


# Feedback
def user_feedback(request):
    feedback_data = FeedBackUser.objects.all()
    return render(request, "user_template/user_feedback.html", {"feedback_data": feedback_data})


def user_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("user_feedback_save"))
    else:
        name = request.POST.get("name")
        feedback_msg=request.POST.get("feedback_msg")

        try:
            feedback = FeedBackUser(name=name, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("user_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("user_feedback"))
