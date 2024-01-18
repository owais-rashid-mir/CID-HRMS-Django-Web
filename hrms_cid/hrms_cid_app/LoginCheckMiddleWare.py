# Middleware is a framework used for Django's request/response processing.
# When a user requests to access a URL , it will first come to Middleware and then the request will be processed.

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
import logging
from datetime import datetime

# Define the log_user_activity function directly in the middleware file
user_activity_logger = logging.getLogger('user_activity')


# Details to store in the "user_activity.log" log file (defined in settings.py)
def log_user_activity(request, user, activity_type, details):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = request.META.get('REMOTE_ADDR', 'Unknown')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')     # contains information about the user's device and browser.
    http_method = request.method
    status_code = getattr(request, 'status_code', None)
    user_activity_logger.info(
        f'{timestamp} - {activity_type} - User: {user.username} - IP: {ip_address} - User-Agent: {user_agent} - Method: {http_method} - Status Code: {status_code} - Details: {details}')


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        # Logging - Log user activity for every view accessed
        if user.is_authenticated:
            activity_type = 'View'
            details = f'User accessed {request.path}'
            log_user_activity(request, user, activity_type, details)

        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "hrms_cid_app.AdminViews":
                    pass
                elif modulename == "hrms_cid_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))

            elif user.user_type == "2":
                if modulename == "hrms_cid_app.UserViews":
                    pass
                elif modulename == "hrms_cid_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("user_home"))

            elif user.user_type == "3":
                if modulename == "hrms_cid_app.SectionHeadViews":
                    pass
                elif modulename == "hrms_cid_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("section_head_home"))

            elif user.user_type == "4":
                if modulename == "hrms_cid_app.DivisionHeadViews":
                    pass
                elif modulename == "hrms_cid_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("division_head_home"))

            elif user.user_type == "5":
                if modulename == "hrms_cid_app.DdoViews":
                    pass
                elif modulename == "hrms_cid_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("ddo_home"))

            elif user.user_type == "6":
                if modulename == "hrms_cid_app.SpecialDgViews":
                    pass
                elif modulename == "hrms_cid_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("special_dg_home"))

            elif user.user_type == "7":
                if modulename == "hrms_cid_app.IgpViews":
                    pass
                elif modulename == "hrms_cid_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("igp_home"))

            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login") or modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites" or modulename == "hrms_cid_app.views":
                pass
            else:
                return HttpResponseRedirect(reverse("showIndexHomepage"))


