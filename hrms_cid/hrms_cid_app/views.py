import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from hrms_cid_app.EmailBackEnd import EmailBackEnd


# Create your views here.
def showDemoPage(request):
    return render(request, "demo.html")


def ShowLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    # if method is not POST, print error message
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    # If method is Post, allow login:
    else:
        # "email" and "password" are the names of email and password input fields in login_page.html.
        # EmailBackEnd is in EmailBackEnd.py file
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user != None:
            login(request, user)
            # On login success, redirecting user to admin homepage
            return HttpResponseRedirect('/admin_home')
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + " usertype : " + str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)     # logout is a built-in method
    return HttpResponseRedirect("/")    # Redirecting user back to login page
