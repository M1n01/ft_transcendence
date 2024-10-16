from accounts.models import FtUser
from django.db import models

# from datetime import datetime, timezone, timedelta
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
import uuid

# Create your models here.


class NotificationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    jp = models.TextField()
    en = models.TextField()
    fr = models.TextField()
    link = models.TextField(null=True)
    created_at = models.DateTimeField(
        verbose_name=_("作成日"), auto_now_add=True, null=True
    )
    expired_at = models.DateTimeField(verbose_name=_("有効期限"), null=True)

    def __str__(self):
        lang = get_language()
        if lang == "jp":
            return f"NotificationMessage - {self.jp[:50]}"
        elif lang == "en":
            return f"NotificationMessage - {self.en[:50]}"
        elif lang == "fr":
            return f"NotificationMessage - {self.fr[:50]}"


class UserNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        FtUser, on_delete=models.CASCADE, related_name="user_notifications"
    )
    message = models.ForeignKey(NotificationMessage, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name=_("作成日"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("変更日"), auto_now=True)

    # class Meta:
    #    constraints = [
    #        models.UniqueConstraint(fields=["user", "message"], name="message_unique"),
    #    ]

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message.message[:20]}"
