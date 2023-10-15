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

from hrms_cid_app import views, AdminViews, UserViews, RegistrationViews
from hrms_cid import settings

urlpatterns = [
                  # showDemoPage, GetUsersDetails, logout_user etc functions are defined in views.py file
                  # Setting showIndexHomepage(index.html) as my homepage
                  path('', views.showIndexHomepage, name="showIndexHomepage"),
                  path('index_homepage', views.showIndexHomepage),

                  # path('demo', views.showDemoPage),
                  path('show_login', views.ShowLoginPage, name="show_login"),
                  path('admin/', admin.site.urls),
                  path('get_user_details', views.GetUserDetails),
                  path('logout_user', views.logout_user, name="logout"),
                  path('doLogin', views.doLogin, name="do_login"),
                  path('admin_home', AdminViews.admin_home, name="admin_home"),
                  # AdminViews.py is a file. admin_home is its fxn.

                  path('add_user', AdminViews.add_user, name="add_user"),  # Check AdminViews.py
                  path('add_user_save', AdminViews.add_user_save, name="add_user_save"),

                  # Section URLs - Admin side
                  path('add_section', AdminViews.add_section, name="add_section"),  # Check AdminViews.py
                  path('add_section_save', AdminViews.add_section_save, name="add_section_save"),
                  path('manage_section', AdminViews.manage_section, name="manage_section"),
                  path('edit_section/<str:section_id>', AdminViews.edit_section, name="edit_section"),
                  path('edit_section_save', AdminViews.edit_section_save, name="edit_section_save"),
                  path('delete_section/<int:section_id>/', AdminViews.delete_section, name='delete_section'),

                  # Employee Supervisor URLs - Admin side
                  path('add_supervisor', AdminViews.add_supervisor, name="add_supervisor"),
                  path('add_supervisor_save', AdminViews.add_supervisor_save, name="add_supervisor_save"),
                  path('manage_supervisor', AdminViews.manage_supervisor, name="manage_supervisor"),
                  path('edit_supervisor/<str:supervisor_id>', AdminViews.edit_supervisor, name="edit_supervisor"),
                  path('edit_supervisor_save', AdminViews.edit_supervisor_save, name="edit_supervisor_save"),
                  path('delete_supervisor/<int:supervisor_id>/', AdminViews.delete_supervisor,
                       name='delete_supervisor'),

                  # Employee URLs - Admin side
                  path('add_employee', AdminViews.add_employee, name="add_employee"),
                  path('add_employee_save', AdminViews.add_employee_save, name="add_employee_save"),
                  path('manage_employee', AdminViews.manage_employee, name="manage_employee"),
                  path('edit_employee/<str:emp_id>', AdminViews.edit_employee, name="edit_employee"),
                  path('edit_employee_save', AdminViews.edit_employee_save, name="edit_employee_save"),
                  path('delete_employee/<int:emp_id>/', AdminViews.delete_employee, name='delete_employee'),
                  # path('view_all_employee/<str:emp_id>', AdminViews.view_all_employee, name="view_all_employee"),
                  path('view_all_employee/<int:emp_id>/', AdminViews.view_all_employee, name="view_all_employee"),

                  path('manage_user', AdminViews.manage_user, name="manage_user"),
                  path('edit_user/<str:id>', AdminViews.edit_user, name="edit_user"),  # id from User table.
                  path('edit_user_save', AdminViews.edit_user_save, name="edit_user_save"),

                  path('user_feedback_message', AdminViews.user_feedback_message, name="user_feedback_message"),
                  path('user_feedback_message_replied', AdminViews.user_feedback_message_replied,
                       name="user_feedback_message_replied"),

                  path('user_leave_view', AdminViews.user_leave_view, name="user_leave_view"),
                  path('user_disapprove_leave/<str:leave_id>', AdminViews.user_disapprove_leave,
                       name="user_disapprove_leave"),
                  path('user_approve_leave/<str:leave_id>', AdminViews.user_approve_leave, name="user_approve_leave"),

                  # Rank URLs - Admin side
                  path('add_rank', AdminViews.add_rank, name="add_rank"),
                  path('add_rank_save', AdminViews.add_rank_save, name="add_rank_save"),
                  path('manage_rank', AdminViews.manage_rank, name="manage_rank"),
                  path('edit_rank/<str:rank_id>', AdminViews.edit_rank, name="edit_rank"),
                  path('edit_rank_save', AdminViews.edit_rank_save, name="edit_rank_save"),
                  path('delete_rank/<int:rank_id>/', AdminViews.delete_rank, name='delete_rank'),

                  # Division URLs - Admin side
                  path('add_division', AdminViews.add_division, name="add_division"),
                  path('add_division_save', AdminViews.add_division_save, name="add_division_save"),
                  path('manage_division', AdminViews.manage_division, name="manage_division"),
                  path('edit_division/<str:division_id>', AdminViews.edit_division, name="edit_division"),
                  path('edit_division_save', AdminViews.edit_division_save, name="edit_division_save"),
                  path('delete_division/<int:division_id>/', AdminViews.delete_division, name='delete_division'),

                  # Security Question URLs - Admin side
                  path('add_admin_security_question', AdminViews.add_admin_security_question, name="add_admin_security_question"),
                  path('add_admin_security_question_save', AdminViews.add_admin_security_question_save, name="add_admin_security_question_save"),
                  path('manage_admin_security_question', AdminViews.manage_admin_security_question, name="manage_admin_security_question"),
                  path('edit_admin_security_question/<str:id>', AdminViews.edit_admin_security_question, name="edit_admin_security_question"),
                  path('edit_admin_security_question_save', AdminViews.edit_admin_security_question_save, name="edit_admin_security_question_save"),
                  path('delete_admin_security_question/<int:id>/', AdminViews.delete_admin_security_question, name='delete_admin_security_question'),


                  # Security Question URLs - User side
                  path('add_user_security_question', AdminViews.add_user_security_question, name="add_user_security_question"),
                  path('add_user_security_question_save', AdminViews.add_user_security_question_save, name="add_user_security_question_save"),
                  path('manage_user_security_question', AdminViews.manage_user_security_question, name="manage_user_security_question"),
                  path('edit_user_security_question/<str:id>', AdminViews.edit_user_security_question, name="edit_user_security_question"),
                  path('edit_user_security_question_save', AdminViews.edit_user_security_question_save, name="edit_user_security_question_save"),
                  path('delete_user_security_question/<int:id>/', AdminViews.delete_user_security_question, name='delete_user_security_question'),

                  # --------------------------- User URL Path --------------------------------
                  path('user_home', UserViews.user_home, name="user_home"),

                  path('user_apply_leave', UserViews.user_apply_leave, name="user_apply_leave"),
                  path('user_apply_leave_save', UserViews.user_apply_leave_save, name="user_apply_leave_save"),

                  path('user_feedback', UserViews.user_feedback, name="user_feedback"),
                  path('user_feedback_save', UserViews.user_feedback_save, name="user_feedback_save"),


                  # --------------------------- Registration URL Path --------------------------------
                  path('registration', RegistrationViews.registration, name="registration"),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
