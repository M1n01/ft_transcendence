from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FtUser


@receiver(post_save, sender=FtUser)
def execute_after_create(sender, instance, created, **kwargs):
    if created:
        pass
