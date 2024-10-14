from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Tournament
from notification.models import UserNotification, NotificationMessage
from friend.models import Friendships
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Tournament)
def execute_after_create(sender, instance, created, **kwargs):
    if created:
        try:
            message = NotificationMessage.objects.get(name="new_tournament")
            if message is None:
                return
            if instance.is_only_friend is False:
                return
            friends = Friendships.objects.filter(user=instance.organizer)
            for friend in friends:
                UserNotification.objects.create(user=friend.friend, message=message)
        except Exception as e:
            logger.error(f"Error:{e}")
