from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Tournament
from notification.models import UserNotification, NotificationMessage
from friend.models import Friendships


@receiver(post_save, sender=Tournament)
def execute_after_create(sender, instance, created, **kwargs):
    print("tournament signal execute after create No.1")
    if created:
        print("tournament signal execute after create No.2")
        message = NotificationMessage.objects.get(name="new_tournament")
        if instance.is_only_friend is False:
            return
        print("tournament signal execute after create No.3")
        friends = Friendships.objects.filter(user=instance.organizer)
        for friend in friends:
            UserNotification.objects.create(user=friend.friend, message=message)
