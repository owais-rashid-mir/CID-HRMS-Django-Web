import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from hrms_cid_app.EmailBackEnd import EmailBackEnd


# Create your views here.
def showIndexHomepage(request):
    return render(request, "index.html")


# About page
def about(request):
    return render(request, "about.html")


# About the Developer page
def about_the_dev(request):
    return render(request, "about_the_dev.html")


def ShowLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))

        if user is not None:
            login(request, user)

            if user.user_type == "1":
                # Admin login
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                # User login
                return HttpResponseRedirect(reverse("user_home"))
            elif user.user_type == "3":
                # Section Head login
                return HttpResponseRedirect(reverse("section_head_home"))
            elif user.user_type == "4":
                # Division Head login
                return HttpResponseRedirect(reverse("division_head_home"))
            elif user.user_type == "5":
                # DDO login
                return HttpResponseRedirect(reverse("ddo_home"))
            elif user.user_type == "6":
                # Special DG login
                return HttpResponseRedirect(reverse("special_dg_home"))
            elif user.user_type == "7":
                # IGP login
                return HttpResponseRedirect(reverse("igp_home"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/show_login")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + " usertype : " + str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)  # logout is a built-in method
    return HttpResponseRedirect("/")  # Redirecting user back to login page
