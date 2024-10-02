from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Tournament
from notification.models import UserNotification, NotificationMessage
from friend.models import Friendships


@receiver(post_save, sender=Tournament)
def execute_after_create(sender, instance, created, **kwargs):
    if created:
        message = NotificationMessage.objects.get(name="new_tournament")
        if instance.is_only_friend is False:
            return
        friends = Friendships.objects.filter(user=instance.organizer)
        for friend in friends:
            UserNotification.objects.create(user=friend.friend, message=message)
