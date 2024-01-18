# For login authentication

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Fetching the user from database
            user = UserModel.objects.get(email=username)
            # print("User Type:", user.user_type)  # Add this line to print the user type
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
