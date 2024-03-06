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

from hrms_cid_app import views, AdminViews, UserViews, RegistrationViews, SectionHeadViews, DivisionHeadViews, DdoViews, \
    SpecialDgViews, IgpViews
from hrms_cid import settings

urlpatterns = [
                  # showDemoPage, GetUsersDetails, logout_user etc functions are defined in views.py file
                  # Setting showIndexHomepage(index.html) as my homepage
                  path('', views.showIndexHomepage, name="showIndexHomepage"),
                  path('index_homepage', views.showIndexHomepage),


                  # path('demo', views.showDemoPage),
                  path('show_login', views.ShowLoginPage, name="show_login"),
                  path('about', views.about, name="about"),
                  path('about_the_dev', views.about_the_dev, name="about_the_dev"),
                  path('admin/', admin.site.urls),
                  path('get_user_details', views.GetUserDetails),
                  path('logout_user', views.logout_user, name="logout"),
                  path('doLogin', views.doLogin, name="do_login"),

                  # AdminViews.py is a file. admin_home is its function or method.
                  path('admin_home', AdminViews.admin_home, name="admin_home"),

                  # Add Admin URLs - Admin Side
                  path('add_admin', AdminViews.add_admin, name="add_admin"),  # Check AdminViews.py
                  path('add_admin_save', AdminViews.add_admin_save, name="add_admin_save"),
                  path('manage_admin', AdminViews.manage_admin, name="manage_admin"),
                  path('edit_admin/<int:id>', AdminViews.edit_admin, name="edit_admin"),  # id from Admin table.
                  path('edit_admin_save', AdminViews.edit_admin_save, name="edit_admin_save"),
                  path('delete_admin/<int:id>/', AdminViews.delete_admin, name='delete_admin'),


                  # Add User URLs - Admin Side
                  path('add_user', AdminViews.add_user, name="add_user"),  # Check AdminViews.py
                  path('add_user_save', AdminViews.add_user_save, name="add_user_save"),
                  path('manage_user', AdminViews.manage_user, name="manage_user"),
                  path('edit_user/<int:id>', AdminViews.edit_user, name="edit_user"),  # id from User table.
                  path('edit_user_save', AdminViews.edit_user_save, name="edit_user_save"),
                  path('delete_user/<int:id>/', AdminViews.delete_user, name='delete_user'),


                  # Add Section Head URLs - Admin Side
                  path('add_section_head', AdminViews.add_section_head, name="add_section_head"),
                  path('add_section_head_save', AdminViews.add_section_head_save, name="add_section_head_save"),
                  path('manage_section_head', AdminViews.manage_section_head, name="manage_section_head"),
                  path('edit_section_head/<int:admin_id>', AdminViews.edit_section_head, name="edit_section_head"),
                  path('edit_section_head_save', AdminViews.edit_section_head_save, name="edit_section_head_save"),
                  path('delete_section_head/<int:id>/', AdminViews.delete_section_head, name='delete_section_head'),


                  # Add Division Head URLs - Admin Side
                  path('add_division_head', AdminViews.add_division_head, name="add_division_head"),
                  path('add_division_head_save', AdminViews.add_division_head_save, name="add_division_head_save"),
                  path('manage_division_head', AdminViews.manage_division_head, name="manage_division_head"),
                  path('edit_division_head/<int:admin_id>', AdminViews.edit_division_head, name="edit_division_head"),
                  path('edit_division_head_save', AdminViews.edit_division_head_save, name="edit_division_head_save"),
                  path('delete_division_head/<int:id>/', AdminViews.delete_division_head, name='delete_division_head'),


                  # Add DDO URLs - Admin Side
                  path('add_ddo', AdminViews.add_ddo, name="add_ddo"),
                  path('add_ddo_save', AdminViews.add_ddo_save, name="add_ddo_save"),
                  path('manage_ddo', AdminViews.manage_ddo, name="manage_ddo"),
                  path('edit_ddo/<int:id>', AdminViews.edit_ddo, name="edit_ddo"),
                  path('edit_ddo_save', AdminViews.edit_ddo_save, name="edit_ddo_save"),
                  path('delete_ddo/<int:id>/', AdminViews.delete_ddo, name='delete_ddo'),


                  # Add Special DG URLs - Admin Side
                  path('add_special_dg', AdminViews.add_special_dg, name="add_special_dg"),
                  path('add_special_dg_save', AdminViews.add_special_dg_save, name="add_special_dg_save"),
                  path('manage_special_dg', AdminViews.manage_special_dg, name="manage_special_dg"),
                  path('edit_special_dg/<int:id>', AdminViews.edit_special_dg, name="edit_special_dg"),
                  path('edit_special_dg_save', AdminViews.edit_special_dg_save, name="edit_special_dg_save"),
                  path('delete_special_dg/<int:id>/', AdminViews.delete_special_dg, name='delete_special_dg'),


                  # Add IGP URLs - Admin Side
                  path('add_igp', AdminViews.add_igp, name="add_igp"),
                  path('add_igp_save', AdminViews.add_igp_save, name="add_igp_save"),
                  path('manage_igp', AdminViews.manage_igp, name="manage_igp"),
                  path('edit_igp/<int:id>', AdminViews.edit_igp, name="edit_igp"),
                  path('edit_igp_save', AdminViews.edit_igp_save, name="edit_igp_save"),
                  path('delete_igp/<int:id>/', AdminViews.delete_igp, name='delete_igp'),


                  # Section URLs - Admin side
                  path('add_section', AdminViews.add_section, name="add_section"),  # Check AdminViews.py
                  path('add_section_save', AdminViews.add_section_save, name="add_section_save"),
                  path('manage_section', AdminViews.manage_section, name="manage_section"),
                  path('edit_section/<str:section_id>', AdminViews.edit_section, name="edit_section"),
                  path('edit_section_save', AdminViews.edit_section_save, name="edit_section_save"),
                  path('delete_section/<int:section_id>/', AdminViews.delete_section, name='delete_section'),
                  path('view_all_section_details/<int:section_id>/', AdminViews.view_all_section_details, name='view_all_section_details'),


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
                  path('view_all_employee/<int:emp_id>/', AdminViews.view_all_employee, name="view_all_employee"),


                  # Feedback - Admin Side
                  path('user_feedback_message', AdminViews.user_feedback_message, name="user_feedback_message"),
                  path('user_feedback_message_replied', AdminViews.user_feedback_message_replied,
                       name="user_feedback_message_replied"),


                  # Leaves - Admin Side
                  path('view_all_dept_leaves', AdminViews.view_all_dept_leaves, name="view_all_dept_leaves"),
                  path('admin_apply_leave', AdminViews.admin_apply_leave, name="admin_apply_leave"),
                  path('admin_apply_leave_save', AdminViews.admin_apply_leave_save, name="admin_apply_leave_save"),
                  path('admin_leave_history', AdminViews.admin_leave_history, name="admin_leave_history"),
                  path('edit_leave_counters/', AdminViews.edit_leave_counters, name='edit_leave_counters'),


                  # Rank URLs - Admin side
                  path('add_rank', AdminViews.add_rank, name="add_rank"),
                  path('add_rank_save', AdminViews.add_rank_save, name="add_rank_save"),
                  path('manage_rank', AdminViews.manage_rank, name="manage_rank"),
                  path('edit_rank/<str:rank_id>', AdminViews.edit_rank, name="edit_rank"),
                  path('edit_rank_save', AdminViews.edit_rank_save, name="edit_rank_save"),
                  path('delete_rank/<int:rank_id>/', AdminViews.delete_rank, name='delete_rank'),
                  path('view_all_rank_details/<int:rank_id>/', AdminViews.view_all_rank_details, name='view_all_rank_details'),


                  # Division URLs - Admin side
                  path('add_division', AdminViews.add_division, name="add_division"),
                  path('add_division_save', AdminViews.add_division_save, name="add_division_save"),
                  path('manage_division', AdminViews.manage_division, name="manage_division"),
                  path('edit_division/<str:division_id>', AdminViews.edit_division, name="edit_division"),
                  path('edit_division_save', AdminViews.edit_division_save, name="edit_division_save"),
                  path('delete_division/<int:division_id>/', AdminViews.delete_division, name='delete_division'),
                  path('view_all_division_details/<int:division_id>/', AdminViews.view_all_division_details, name='view_all_division_details'),


                  # Security Question URLs for Admin - Admin side
                  path('add_admin_security_question', AdminViews.add_admin_security_question,
                       name="add_admin_security_question"),
                  path('add_admin_security_question_save', AdminViews.add_admin_security_question_save,
                       name="add_admin_security_question_save"),
                  path('manage_admin_security_question', AdminViews.manage_admin_security_question,
                       name="manage_admin_security_question"),
                  path('edit_admin_security_question/<str:id>', AdminViews.edit_admin_security_question,
                       name="edit_admin_security_question"),
                  path('edit_admin_security_question_save', AdminViews.edit_admin_security_question_save,
                       name="edit_admin_security_question_save"),
                  path('delete_admin_security_question/<int:id>/', AdminViews.delete_admin_security_question,
                       name='delete_admin_security_question'),


                  # Security Question URLs for User - Admin side
                  path('add_user_security_question', AdminViews.add_user_security_question,
                       name="add_user_security_question"),
                  path('add_user_security_question_save', AdminViews.add_user_security_question_save,
                       name="add_user_security_question_save"),
                  path('manage_user_security_question', AdminViews.manage_user_security_question,
                       name="manage_user_security_question"),
                  path('edit_user_security_question/<str:id>', AdminViews.edit_user_security_question,
                       name="edit_user_security_question"),
                  path('edit_user_security_question_save', AdminViews.edit_user_security_question_save,
                       name="edit_user_security_question_save"),
                  path('delete_user_security_question/<int:id>/', AdminViews.delete_user_security_question,
                       name='delete_user_security_question'),


                  # Search - Admin Side
                  path('employee_search/', AdminViews.employee_search, name='employee_search'),


                  # My profile - Admin Side
                  path('my_profile_admin/', AdminViews.my_profile_admin, name='my_profile_admin'),


                  # Profile Correction Request (PCR) - Admin Side
                  path('pcr_msg', AdminViews.pcr_msg, name="pcr_msg"),
                  path('pcr_msg_replied', AdminViews.pcr_msg_replied,
                       name="pcr_msg_replied"),

                  # Archived Employees
                  path('archive_employee/<int:emp_id>/', AdminViews.archive_employee, name='archive_employee'),
                  path('manage_archived_employee', AdminViews.manage_archived_employee, name="manage_archived_employee"),
                  path('view_all_archived_employee/<int:emp_id>/', AdminViews.view_all_archived_employee, name="view_all_archived_employee"),
                  path('delete_archived_employee/<int:emp_id>/', AdminViews.delete_archived_employee, name='delete_archived_employee'),

                  # Export employees to Excel
                  path('export-employees/', AdminViews.export_employees, name='export_employees'),


                  # --------------------------- User URL Path --------------------------------
                  path('user_home', UserViews.user_home, name="user_home"),

                  path('user_apply_leave', UserViews.user_apply_leave, name="user_apply_leave"),
                  path('user_apply_leave_save', UserViews.user_apply_leave_save, name="user_apply_leave_save"),
                  path('user_leave_history', UserViews.user_leave_history, name="user_leave_history"),

                  path('user_feedback', UserViews.user_feedback, name="user_feedback"),
                  path('user_feedback_save', UserViews.user_feedback_save, name="user_feedback_save"),
                  path('user_feedback_history', UserViews.user_feedback_history, name="user_feedback_history"),

                  path('view_all_employee_user/<int:emp_id>/', UserViews.view_all_employee_user, name="view_all_employee_user"),
                  path('my_profile_user/', UserViews.my_profile_user, name='my_profile_user'),

                  path('profile_corr_req_user', UserViews.profile_corr_req_user, name="profile_corr_req_user"),
                  path('profile_corr_req_user_save', UserViews.profile_corr_req_user_save, name="profile_corr_req_user_save"),
                  path('profile_corr_req_user_history', UserViews.profile_corr_req_user_history, name="profile_corr_req_user_history"),


                  # --------------------------- Section Head URL Path --------------------------------
                  path('section_head_home', SectionHeadViews.section_head_home, name="section_head_home"),
                  path('manage_leaves_sh', SectionHeadViews.manage_leaves_sh, name="manage_leaves_sh"),
                  path('disapprove_leave_sh/<str:leave_id>', SectionHeadViews.disapprove_leave_sh,
                       name="disapprove_leave_sh"),
                  path('approve_leave_sh/<str:leave_id>', SectionHeadViews.approve_leave_sh, name="approve_leave_sh"),
                  path('sh_apply_leave', SectionHeadViews.sh_apply_leave, name="sh_apply_leave"),
                  path('sh_apply_leave_save', SectionHeadViews.sh_apply_leave_save, name="sh_apply_leave_save"),
                  path('sh_leave_history', SectionHeadViews.sh_leave_history, name="sh_leave_history"),

                  path('view_all_employee_sh/<int:emp_id>/', SectionHeadViews.view_all_employee_sh, name="view_all_employee_sh"),
                  path('my_profile_sh/', SectionHeadViews.my_profile_sh, name='my_profile_sh'),

                  path('view_all_section_details_sh/<int:section_id>/', SectionHeadViews.view_all_section_details_sh, name="view_all_section_details_sh"),
                  path('my_section_sh/', SectionHeadViews.my_section_sh, name='my_section_sh'),

                  path('sh_feedback', SectionHeadViews.sh_feedback, name="sh_feedback"),
                  path('sh_feedback_save', SectionHeadViews.sh_feedback_save, name="sh_feedback_save"),
                  path('sh_feedback_history', SectionHeadViews.sh_feedback_history, name="sh_feedback_history"),

                  path('profile_corr_req_sh', SectionHeadViews.profile_corr_req_sh, name="profile_corr_req_sh"),
                  path('profile_corr_req_sh_save', SectionHeadViews.profile_corr_req_sh_save, name="profile_corr_req_sh_save"),
                  path('profile_corr_req_sh_history', SectionHeadViews.profile_corr_req_sh_history, name="profile_corr_req_sh_history"),


                  # --------------------------- Division Head URL Path --------------------------------
                  path('division_head_home', DivisionHeadViews.division_head_home, name="division_head_home"),
                  path('manage_leaves_dh', DivisionHeadViews.manage_leaves_dh, name="manage_leaves_dh"),
                  path('disapprove_leave_dh/<str:leave_id>', DivisionHeadViews.disapprove_leave_dh,
                       name="disapprove_leave_dh"),
                  path('approve_leave_dh/<str:leave_id>', DivisionHeadViews.approve_leave_dh, name="approve_leave_dh"),
                  path('override_disapprove_leave_dh/<str:leave_id>', DivisionHeadViews.override_disapprove_leave_dh,
                       name="override_disapprove_leave_dh"),
                  path('override_approve_leave_dh/<str:leave_id>', DivisionHeadViews.override_approve_leave_dh, name="override_approve_leave_dh"),
                  path('dh_apply_leave', DivisionHeadViews.dh_apply_leave, name="dh_apply_leave"),
                  path('dh_apply_leave_save', DivisionHeadViews.dh_apply_leave_save, name="dh_apply_leave_save"),
                  path('dh_leave_history', DivisionHeadViews.dh_leave_history, name="dh_leave_history"),

                  path('view_all_employee_dh/<int:emp_id>/', DivisionHeadViews.view_all_employee_dh, name="view_all_employee_dh"),
                  path('my_profile_dh/', DivisionHeadViews.my_profile_dh, name='my_profile_dh'),

                  path('view_all_division_details_dh/<int:division_id>/', DivisionHeadViews.view_all_division_details_dh, name="view_all_division_details_dh"),
                  path('my_division_dh/', DivisionHeadViews.my_division_dh, name='my_division_dh'),

                  path('dh_feedback', DivisionHeadViews.dh_feedback, name="dh_feedback"),
                  path('dh_feedback_save', DivisionHeadViews.dh_feedback_save, name="dh_feedback_save"),
                  path('dh_feedback_history', DivisionHeadViews.dh_feedback_history, name="dh_feedback_history"),

                  path('profile_corr_req_dh', DivisionHeadViews.profile_corr_req_dh, name="profile_corr_req_dh"),
                  path('profile_corr_req_dh_save', DivisionHeadViews.profile_corr_req_dh_save, name="profile_corr_req_dh_save"),
                  path('profile_corr_req_dh_history', DivisionHeadViews.profile_corr_req_dh_history, name="profile_corr_req_dh_history"),


                  # --------------------------- DDO URL Path --------------------------------
                  path('ddo_home', DdoViews.ddo_home, name="ddo_home"),
                  path('manage_leaves_ddo', DdoViews.manage_leaves_ddo, name="manage_leaves_ddo"),
                  path('disapprove_leave_ddo/<str:leave_id>', DdoViews.disapprove_leave_ddo,
                       name="disapprove_leave_ddo"),
                  path('approve_leave_ddo/<str:leave_id>', DdoViews.approve_leave_ddo, name="approve_leave_ddo"),
                  path('override_disapprove_leave_ddo/<str:leave_id>', DdoViews.override_disapprove_leave_ddo,
                       name="override_disapprove_leave_ddo"),
                  path('override_approve_leave_ddo/<str:leave_id>', DdoViews.override_approve_leave_ddo, name="override_approve_leave_ddo"),
                  path('ddo_apply_leave', DdoViews.ddo_apply_leave, name="ddo_apply_leave"),
                  path('ddo_apply_leave_save', DdoViews.ddo_apply_leave_save, name="ddo_apply_leave_save"),
                  path('ddo_leave_history', DdoViews.ddo_leave_history, name="ddo_leave_history"),

                  path('view_all_employee_ddo/<int:emp_id>/', DdoViews.view_all_employee_ddo, name="view_all_employee_ddo"),
                  path('my_profile_ddo/', DdoViews.my_profile_ddo, name='my_profile_ddo'),

                  path('ddo_feedback', DdoViews.ddo_feedback, name="ddo_feedback"),
                  path('ddo_feedback_save', DdoViews.ddo_feedback_save, name="ddo_feedback_save"),
                  path('ddo_feedback_history', DdoViews.ddo_feedback_history, name="ddo_feedback_history"),

                  path('profile_corr_req_ddo', DdoViews.profile_corr_req_ddo, name="profile_corr_req_ddo"),
                  path('profile_corr_req_ddo_save', DdoViews.profile_corr_req_ddo_save, name="profile_corr_req_ddo_save"),
                  path('profile_corr_req_ddo_history', DdoViews.profile_corr_req_ddo_history, name="profile_corr_req_ddo_history"),


                  # --------------------------- Special DG URL Path --------------------------------
                  path('special_dg_home', SpecialDgViews.special_dg_home, name="special_dg_home"),
                  path('manage_leaves_sp_dg', SpecialDgViews.manage_leaves_sp_dg, name="manage_leaves_sp_dg"),

                  path('disapprove_leave_sp_dg/<str:leave_id>', SpecialDgViews.disapprove_leave_sp_dg,
                       name="disapprove_leave_sp_dg"),
                  path('approve_leave_sp_dg/<str:leave_id>', SpecialDgViews.approve_leave_sp_dg, name="approve_leave_sp_dg"),
                  path('override_disapprove_leave_sp_dg/<str:leave_id>', SpecialDgViews.override_disapprove_leave_sp_dg,
                       name="override_disapprove_leave_sp_dg"),
                  path('override_approve_leave_sp_dg/<str:leave_id>', SpecialDgViews.override_approve_leave_sp_dg, name="override_approve_leave_sp_dg"),
                  path('sp_dg_apply_leave', SpecialDgViews.sp_dg_apply_leave, name="sp_dg_apply_leave"),
                  path('sp_dg_apply_leave_save', SpecialDgViews.sp_dg_apply_leave_save, name="sp_dg_apply_leave_save"),
                  path('sp_dg_leave_history', SpecialDgViews.sp_dg_leave_history, name="sp_dg_leave_history"),

                  path('view_all_employee_sp_dg/<int:emp_id>/', SpecialDgViews.view_all_employee_sp_dg, name="view_all_employee_sp_dg"),
                  path('my_profile_sp_dg/', SpecialDgViews.my_profile_sp_dg, name='my_profile_sp_dg'),

                  path('sp_dg_feedback', SpecialDgViews.sp_dg_feedback, name="sp_dg_feedback"),
                  path('sp_dg_feedback_save', SpecialDgViews.sp_dg_feedback_save, name="sp_dg_feedback_save"),
                  path('sp_dg_feedback_history', SpecialDgViews.sp_dg_feedback_history, name="sp_dg_feedback_history"),

                  path('profile_corr_req_sp_dg', SpecialDgViews.profile_corr_req_sp_dg, name="profile_corr_req_sp_dg"),
                  path('profile_corr_req_sp_dg_save', SpecialDgViews.profile_corr_req_sp_dg_save, name="profile_corr_req_sp_dg_save"),
                  path('profile_corr_req_sp_dg_history', SpecialDgViews.profile_corr_req_sp_dg_history, name="profile_corr_req_sp_dg_history"),


                  # --------------------------- IGP URL Path --------------------------------
                  path('igp_home', IgpViews.igp_home, name="igp_home"),
                  path('view_all_employee_igp/<int:emp_id>/', IgpViews.view_all_employee_igp, name="view_all_employee_igp"),
                  path('my_profile_igp/', IgpViews.my_profile_igp, name='my_profile_igp'),

                  path('manage_leaves_igp', IgpViews.manage_leaves_igp, name="manage_leaves_igp"),
                  path('disapprove_leave_igp/<str:leave_id>', IgpViews.disapprove_leave_igp,
                       name="disapprove_leave_igp"),
                  path('approve_leave_igp/<str:leave_id>', IgpViews.approve_leave_igp, name="approve_leave_igp"),
                  path('override_disapprove_leave_igp/<str:leave_id>', IgpViews.override_disapprove_leave_igp,
                       name="override_disapprove_leave_igp"),
                  path('override_approve_leave_igp/<str:leave_id>', IgpViews.override_approve_leave_igp, name="override_approve_leave_igp"),
                  path('igp_apply_leave', IgpViews.igp_apply_leave, name="igp_apply_leave"),
                  path('igp_apply_leave_save', IgpViews.igp_apply_leave_save, name="igp_apply_leave_save"),
                  path('igp_leave_history', IgpViews.igp_leave_history, name="igp_leave_history"),

                  path('igp_feedback', IgpViews.igp_feedback, name="igp_feedback"),
                  path('igp_feedback_save', IgpViews.igp_feedback_save, name="igp_feedback_save"),
                  path('igp_feedback_history', IgpViews.igp_feedback_history, name="igp_feedback_history"),

                  path('profile_corr_req_igp', IgpViews.profile_corr_req_igp, name="profile_corr_req_igp"),
                  path('profile_corr_req_igp_save', IgpViews.profile_corr_req_igp_save, name="profile_corr_req_igp_save"),
                  path('profile_corr_req_igp_history', IgpViews.profile_corr_req_igp_history, name="profile_corr_req_igp_history"),

                  # --------------------------- Registration URL Path --------------------------------
                  path('registration', RegistrationViews.registration, name="registration"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
