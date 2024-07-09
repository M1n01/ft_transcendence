from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)
from django.utils.translation import gettext_lazy as _
import logging, datetime


class FtUserManager(BaseUserManager):

    def _create_user(self, email, username, **extra_fields):
        logging.info(f"_create_user")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        # user.set_password(email)
        user.save(using=self._db)

        return user

    def create_user(self, email, username, password, **extra_fields):
        logging.info(f"create_user()")
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email=email,
            username=username,
            # password=password,
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


class FtUser(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group, related_name="ft_user_groups"  # ここで一意の名前を指定します
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="ft_user_permissions"  # ここで一意の名前を指定します
    )

    username = models.CharField(
        verbose_name=_("ft_username"), max_length=32, primary_key=True
    )
    email = models.CharField(verbose_name=_("email"), max_length=256, unique=True)
    # email2 = models.CharField(
    # verbose_name=_("ft_email"), max_length=256, unique=True, null=True
    # )
    # first_name = models.CharField(
    #    verbose_name=_("ft_first_name"),
    #    max_length=150,
    #    null=True,
    #    blank=False,
    # )
    # last_name = models.CharField(
    #    verbose_name=_("ft_last_name"),
    #    max_length=150,
    #    null=True,
    #    blank=False,
    # )
    is_superuser = models.BooleanField(verbose_name=_("ft_is_superuer"), default=False)
    is_staff = models.BooleanField(
        verbose_name=_("ft_staff status"),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_("ft_active"),
        default=True,
    )

    # birth_date = models.DateField(
    #    verbose_name=_("ft_birth_date"), blank=True, null=True
    # )
    created_at = models.DateTimeField(
        verbose_name=_("ft_created_at"),
        # auto_now_add=True,
        default=datetime.datetime.now(),
    )
    updated_at = models.DateTimeField(verbose_name=_("ft_updateded_at"), auto_now=True)

    def __str__(self):
        return f"username={self.username}, email={self.email}"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = FtUserManager()
