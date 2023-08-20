"""
URL configuration for hrms_cid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from hrms_cid import settings
from hrms_cid_app import views, AdminViews

urlpatterns = [
                  # showDemoPage, GetUsersDetails, logout_user etc functions are defined in views.py file
                  path('demo', views.showDemoPage),
                  path('admin/', admin.site.urls),
                  path('', views.ShowLoginPage),
                  path('get_user_details', views.GetUserDetails),
                  path('logout_user', views.logout_user),
                  path('doLogin', views.doLogin),
                  path('admin_home', AdminViews.admin_home),  # AdminViews.py is a file. admin_home is its fxn.
                  path('add_user', AdminViews.add_user, name="add_user"),  # Check AdminViews.py
                  path('add_user_save', AdminViews.add_user_save),
                  path('add_section', AdminViews.add_section, name="add_section"),  # Check AdminViews.py
                  path('add_section_save', AdminViews.add_section_save, name="add_section_save"),
                  path('add_supervisor', AdminViews.add_supervisor, name="add_supervisor"),
                  path('add_supervisor_save', AdminViews.add_supervisor_save, name="add_supervisor_save"),
                  path('add_employee', AdminViews.add_employee, name="add_employee"),
                  path('add_employee_save', AdminViews.add_employee_save, name="add_employee_save"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
