# Middleware is a framework used for Django's request/response processing.
# When a user requests to access a URL , it will first come to Middleware and then the request will be processed.
# Using it for login - so that when a user is logged off, he can't access the admin pages by using the URL of that page.

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "hrms_cid_app.AdminViews":
                    pass
                elif modulename == "hrms_cid_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "hrms_cid_app.UserViews":
                    pass
                elif modulename == "hrms_cid_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("user_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login"):
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))
