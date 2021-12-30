from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    """Extended User Model"""
    pass

    def token(self):
        refresh = RefreshToken.for_user(self)
        token = refresh.access_token
        return str(token)
