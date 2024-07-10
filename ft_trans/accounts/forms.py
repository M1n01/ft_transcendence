from django.contrib.auth.forms import UserCreationForm

# from .modelss import User, FtUser
from .models import FtUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = FtUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
        )


class FtSignUpForm(UserCreationForm):
    class Meta:
        model = FtUser
        fields = (
            # "url",
            "username",
            "email",
            # "email",
            # "first_name",
            # "last_name",
            # "birth_date",
        )
