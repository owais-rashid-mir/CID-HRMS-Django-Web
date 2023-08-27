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
from hrms_cid_app import views, AdminViews, UserViews

urlpatterns = [
                  # showDemoPage, GetUsersDetails, logout_user etc functions are defined in views.py file
                  path('', views.showIndexHomepage),  # Setting showIndexHomepage(index.html) as my homepage
                  path('index_homepage', views.showIndexHomepage),
                  # path('demo', views.showDemoPage),
                  path('show_login', views.ShowLoginPage, name="show_login"),
                  path('admin/', admin.site.urls),
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

                  path('manage_section', AdminViews.manage_section, name="manage_section"),

                  path('manage_employee', AdminViews.manage_employee, name="manage_employee"),

                  path('manage_supervisor', AdminViews.manage_supervisor, name="manage_supervisor"),

                  path('manage_user', AdminViews.manage_user, name="manage_user"),
                  path('edit_user/<str:id>', AdminViews.edit_user, name="edit_user"),  # id from User table.
                  path('edit_user_save', AdminViews.edit_user_save, name="edit_user_save"),

                  path('edit_section/<str:section_id>', AdminViews.edit_section, name="edit_section"),
                  path('edit_section_save', AdminViews.edit_section_save, name="edit_section_save"),

                  path('edit_employee/<str:emp_id>', AdminViews.edit_employee, name="edit_employee"),
                  path('edit_employee_save', AdminViews.edit_employee_save, name="edit_employee_save"),

                  path('edit_supervisor/<str:supervisor_id>', AdminViews.edit_supervisor, name="edit_supervisor"),
                  path('edit_supervisor_save', AdminViews.edit_supervisor_save, name="edit_supervisor_save"),

                  # path('view_all_employee/<str:emp_id>', AdminViews.view_all_employee, name="view_all_employee"),
                  path('view_all_employee/<int:emp_id>/', AdminViews.view_all_employee, name="view_all_employee"),

                  # User URL Path
                  path('user_home', UserViews.user_home, name="user_home"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
