from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Friendships
from notification.models import UserNotification, NotificationMessage


@receiver(post_save, sender=Friendships)
def execute_after_create(sender, instance, created, **kwargs):
    if created:
        # UserNotification.objects.create(user=)
        message = NotificationMessage.objects.get(name="friend_request")
        UserNotification.objects.create(user=instance.friend, message=message)
