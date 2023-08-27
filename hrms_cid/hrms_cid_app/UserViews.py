from django.shortcuts import render


def user_home(request):
    return render(request, "user_template/user_home_template.html")