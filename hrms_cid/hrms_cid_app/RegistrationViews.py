from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import CustomUser, AdminSecurityQuestion, UserSecurityQuestion, Employees, Admin, User


def registration(request):
    # Fetch user and admin security questions
    user_security_questions = UserSecurityQuestion.objects.all()
    admin_security_questions = AdminSecurityQuestion.objects.all()
    employees = Employees.objects.all()

    if request.method == 'POST':
        user_type = int(request.POST['user_type'])
        employee_id = request.POST.get('employee', None)
        password = request.POST['password']
        security_question_id = request.POST.get('security_question', None)
        security_answer = request.POST.get('security_answer', None)

        error_message = None

        try:
            user = CustomUser(username='', email='', password='', user_type=user_type)

            try:
                if user_type == 1:  # Admin user
                    security_question = AdminSecurityQuestion.objects.get(id=security_question_id)
                    if security_question.answer.strip().lower() == security_answer.strip().lower():
                        user.security_question = security_question
                    else:
                        error_message = 'Incorrect security answer for admin.'
                elif user_type == 2:  # Regular user
                    security_question = UserSecurityQuestion.objects.get(id=security_question_id)
                    if security_question.answer.strip().lower() == security_answer.strip().lower():
                        user.security_question = security_question
                    else:
                        error_message = 'Incorrect security answer for user.'
                else:
                    error_message = 'Please provide a valid security question and answer.'
            except (AdminSecurityQuestion.DoesNotExist, UserSecurityQuestion.DoesNotExist):
                error_message = 'Invalid security question.'

            if not error_message:
                # Fetch the selected employee
                employee = Employees.objects.get(emp_id=employee_id)

                # Check if a user with the email already exists
                existing_user = CustomUser.objects.filter(email=employee.email).first()

                if not existing_user:
                    # If the user doesn't exist, create a new one
                    user = CustomUser(username=employee.email, email=employee.email, password='', user_type=user_type)
                    user.set_password(password)
                    user.save()
                else:
                    user = existing_user  # Use the existing user

                # Associate the user with the employee in CustomUser table
                user.employee = employee
                user.save()

                if user_type == 1:  # Admin
                    # Check if an Admin with the provided user_id already exists
                    existing_admin = Admin.objects.filter(admin=user, employee=employee).first()
                    if not existing_admin:
                        # Check if there is an existing Admin record with the same admin_id
                        existing_admin = Admin.objects.filter(admin=user).first()
                        if existing_admin:
                            error_message = 'An Admin with the same admin_id already exists.'
                        else:
                            admin = Admin(admin=user, employee=employee)
                            admin.save()
                elif user_type == 2:  # User
                    # Check if a User with the provided user_id already exists
                    existing_user_user = User.objects.filter(admin=user, employee=employee).first()
                    if not existing_user_user:
                        # Check if there is an existing User record with the same admin_id
                        existing_user_user = User.objects.filter(admin=user).first()
                        if existing_user_user:
                            error_message = 'A User with the same admin_id already exists.'
                        else:
                            user_user = User(admin=user, employee=employee)
                            user_user.save()

                success_message = 'Account created successfully'

                return render(request, 'registration_template/registration.html', {
                    'success_message': success_message,
                    'employees': employees,
                })

        except IntegrityError as e:
            # Capture the error details
            error_message = 'An account with this email or username already exists. Details: {}'.format(str(e))

        return render(request, 'registration_template/registration.html', {
            'user_security_questions_html': ''.join(
                f'<option value="{question.id}">{question.question}</option>' for question in user_security_questions),
            'admin_security_questions_html': ''.join(
                f'<option value="{question.id}">{question.question}</option>' for question in admin_security_questions),
            'employees_html': ''.join(
                f'<option value="{employee.emp_id}">{employee.first_name} {employee.last_name}</option>' for employee in employees),
            'error_message': error_message,
            'employees': employees,
        })

    else:
        return render(request, 'registration_template/registration.html', {
            'user_security_questions_html': ''.join(
                f'<option value="{question.id}">{question.question}</option>' for question in user_security_questions),
            'admin_security_questions_html': ''.join(
                f'<option value="{question.id}">{question.question}</option>' for question in admin_security_questions),
            'employees_html': ''.join(
                f'<option value="{employee.emp_id}">{employee.first_name} {employee.last_name}</option>' for employee in employees),
            'employees': employees,
            'user_type': 2,
        })
