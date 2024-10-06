from django.contrib.auth.backends import ModelBackend
from .models import FtUser, FtTmpUser


class FtUserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        print("FtUser authenticate No.1")
        if email is None or password is None:
            return
        print("FtUser authenticate No.2")
        user = FtUser.objects.get(email=email)
        pwd_valid = user.check_password(password)
        if pwd_valid:
            print("FtUser authenticate No.3")
            return user
        print("FtUser authenticate No.4")
        return None

    def get_user(self, user_id):
        print("FtUser get_user No.1")
        try:
            print("FtUser get_user No.2")
            return FtUser.objects.get(pk=user_id)
        except FtUser.DoesNotExist:
            return None


class TmpUserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        print("FtTmpUser authenticate No.1")
        if email is None or password is None:
            return
        print("FtTmpUser authenticate No.2")
        user = FtTmpUser.objects.get(email=email)
        pwd_valid = user.check_password(password)
        print("FtTmpUser authenticate No.3")
        if pwd_valid:
            print("FtTmpUser authenticate No.4")
            return user
        print("FtTmpUser authenticate No.5")
        return None

    def get_user(self, user_id):
        print("FtTmpUser  get_user No.1")
        try:
            return FtTmpUser.objects.get(pk=user_id)
        except FtTmpUser.DoesNotExist:
            return None
