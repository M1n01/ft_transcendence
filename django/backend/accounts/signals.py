from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .models import FtUser


@receiver(post_save, sender=FtUser)
def execute_after_create(sender, instance, created, **kwargs):
    if created:
        pass


@receiver(user_logged_in)
def execute_after_login(sender, request, user, **kwargs):
    user.is_login = True
    user.save()


@receiver(user_logged_out)
def execute_after_logout(sender, request, user, **kwargs):
    user.is_login = False
    user.save()
