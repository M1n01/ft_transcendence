from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.conf import settings
import logging

from phonenumbers import COUNTRY_CODE_TO_REGION_CODE
import pyotp
import uuid
import random

# import cryptography
from cryptography.fernet import Fernet

SECRET_KEY = getattr(settings, "TWO_FA_AUTH_KEY", None)
cipher_suite = Fernet(SECRET_KEY)
USERNAME_MAX_LEN = getattr(settings, "USERNAME_MAX_LEN", None)
LASTNAME_MAX_LEN = getattr(settings, "LASTNAME_MAX_LEN", None)
FIRSTNAME_MAX_LEN = getattr(settings, "FIRSTNAME_MAX_LEN", None)
EMAIL_MAX_LEN = getattr(settings, "EMAIL_MAX_LEN", None)
PHONE_MAX_LEN = getattr(settings, "PHONE_MAX_LEN", None)


class AuthChoices(models.TextChoices):
    EMAIL = "EMAIL", _("EMail Auth")
    SMS = "SMS", _("SMS Auth")
    APP = "APP", _("App Auth")


COUNTRY_CODE_CHOICES = [
    (f"+{code}", f"+{code} ({region[0]})")
    for code, region in COUNTRY_CODE_TO_REGION_CODE.items()
]


class LanguageChoice(models.TextChoices):
    JP = "jp", _("日本語")
    EN = "en", _("英語")
    FR = "fr", _("フランス語")


# Create your models here.
class FtUserManager(BaseUserManager):
    def _create_user(self, email, username, **extra_fields):
        logging.info("_create_user")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)

        return user

    def create_user(self, email, username, password="", **extra_fields):
        logging.info("create_user()")
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if password == "":
            return self._create_user(
                email=email,
                username=username,
                # password=password,
                **extra_fields,
            )
        else:
            return self._create_user(
                email=email,
                username=username,
                password=password,
                **extra_fields,
            )

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields["is_active"] = True
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )


def user_avatar_path(instance, filename):
    rand = random.randint(0, 1000)
    extension = filename.split(".")[-1]
    filename = f"{rand}/{uuid.uuid4()}.{extension}"

    return f"avatars/user_{instance.id}/{filename}"


class EncryptedField(models.TextField):
    def get_prep_value(self, value):
        if value:
            return cipher_suite.encrypt(value.encode()).decode()
        return value

    def from_db_value(self, value, expression, connection):
        if value:
            return cipher_suite.decrypt(value.encode()).decode()
        return value


class FtUser(AbstractBaseUser, PermissionsMixin):

    groups = models.ManyToManyField(Group, related_name="ft_user_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="ft_user_permissions"
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        verbose_name=_("ユーザー名"), max_length=USERNAME_MAX_LEN, unique=False
    )
    email = models.EmailField(
        verbose_name=_("email"), max_length=EMAIL_MAX_LEN, unique=True
    )
    email42 = models.EmailField(
        verbose_name=_("email42"),
        max_length=EMAIL_MAX_LEN,
        unique=True,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        verbose_name=_("姓"),
        max_length=FIRSTNAME_MAX_LEN,
        null=True,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name=_("名"),
        max_length=LASTNAME_MAX_LEN,
        null=True,
        blank=False,
    )

    country_code = models.CharField(
        choices=COUNTRY_CODE_CHOICES,
        verbose_name=_("国番号"),
        null=True,
        max_length=5,
        default="+81",
    )

    phone = models.CharField(
        verbose_name=_("電話番号"),
        null=True,
        blank=True,
        unique=True,
        max_length=PHONE_MAX_LEN,
    )

    language = models.CharField(
        choices=LanguageChoice,
        verbose_name=_("言語設定"),
        null=False,
        max_length=2,
        default=LanguageChoice.JP,
    )
    match_count = models.IntegerField(
        default=0,
    )
    win_count = models.IntegerField(
        default=0,
    )
    loose_count = models.IntegerField(
        default=0,
    )
    # avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    avatar = models.ImageField(
        verbose_name=_("アバター"),
        upload_to=user_avatar_path,
        default="avatar/default/user.png",
    )
    # two_fa = models.CharField(null=True)
    is_superuser = models.BooleanField(verbose_name=_("is_superuer"), default=False)
    # is_2fa = models.BooleanField(verbose_name=_("is_2fa"), default=False)
    is_ft = models.BooleanField(verbose_name=_("is_ft"), default=False, null=True)
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name=_("is_active"),
        default=True,
    )

    is_login = models.BooleanField(
        verbose_name=_("is_login"),
        default=False,
    )

    birth_date = models.DateField(verbose_name=_("誕生日"), blank=True, null=True)
    auth = models.CharField(
        verbose_name=_("2要素認証"),
        max_length=5,
        choices=AuthChoices,
        default=AuthChoices.APP,
    )
    app_secret = EncryptedField(
        verbose_name=_("App鍵"),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("ft_created_at"),
        null=True,
        blank=False,
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(verbose_name=_("ft_updateded_at"), auto_now=True)

    def __str__(self):
        return f"username={self.username}, email={self.email}"

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = FtUserManager()

    def save(self, *args, **kwargs):
        # 一度だけ実行するように
        if not self.app_secret:
            totp = pyotp.TOTP(pyotp.random_base32())
            secret = totp.secret
            self.app_secret = secret
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None


class FtTmpUserManager(BaseUserManager):
    def _create_user(self, email, username, **extra_fields):
        logging.info("_create_user")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)

        return user

    def create_user(self, email, username, password="", **extra_fields):
        logging.info("create_user()")
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields["is_active"] = True
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self._create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )


class FtTmpUser(AbstractBaseUser, PermissionsMixin):

    groups = models.ManyToManyField(Group, related_name="ft_tmp_user_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="ft_tmp_user_permissions"
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        verbose_name=_("ユーザー名"), max_length=USERNAME_MAX_LEN, unique=False
    )
    email = models.EmailField(
        verbose_name=_("email"), max_length=EMAIL_MAX_LEN, unique=True
    )
    email42 = models.EmailField(
        verbose_name=_("email42"),
        max_length=EMAIL_MAX_LEN,
        unique=True,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        verbose_name=_("姓"),
        max_length=FIRSTNAME_MAX_LEN,
        null=True,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name=_("名"),
        max_length=LASTNAME_MAX_LEN,
        null=True,
        blank=False,
    )

    country_code = models.CharField(
        choices=COUNTRY_CODE_CHOICES,
        verbose_name=_("国番号"),
        null=True,
        max_length=5,
        default="+81",
    )

    phone = models.CharField(
        verbose_name=_("電話番号"),
        null=True,
        blank=True,
        unique=True,
        max_length=PHONE_MAX_LEN,
    )
    language = models.CharField(
        choices=LanguageChoice,
        verbose_name=_("言語設定"),
        null=False,
        max_length=2,
        default=LanguageChoice.JP,
    )

    is_superuser = models.BooleanField(verbose_name=_("is_superuer"), default=False)
    is_ft = models.BooleanField(verbose_name=_("is_ft"), default=False, null=True)
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name=_("is_active"),
        default=True,
    )
    is_login = models.BooleanField(
        verbose_name=_("is_login"),
        default=False,
    )

    birth_date = models.DateField(verbose_name=_("誕生日"), blank=True, null=True)
    auth = models.CharField(
        verbose_name=_("2要素認証"),
        max_length=5,
        choices=AuthChoices,
        default=AuthChoices.APP,
    )
    app_secret = EncryptedField(
        verbose_name=_("App鍵"),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("ft_created_at"),
        null=True,
        blank=False,
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(verbose_name=_("ft_updateded_at"), auto_now=True)

    def __str__(self):
        return f"username={self.username}, email={self.email}"

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = FtTmpUserManager()

    def save(self, *args, **kwargs):
        # 一度だけ実行するように
        if not self.app_secret:
            totp = pyotp.TOTP(pyotp.random_base32())
            secret = totp.secret
            self.app_secret = secret
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
