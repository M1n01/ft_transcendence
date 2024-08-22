from django.contrib.auth.backends import ModelBackend
from .models import FtTmpUser


class TmpUserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        if email is None or password is None:
            return

        print(f"authenticate No.1 {password=}")
        # pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        print("authenticate No.2")
        user = FtTmpUser.objects.get(email=email)
        pwd_valid = user.check_password(password)
        if pwd_valid:
            return user
        print("authenticate No.8")
        return None

    def get_user(self, user_id):
        try:
            return FtTmpUser.objects.get(pk=user_id)
        except FtTmpUser.DoesNotExist:
            return None
