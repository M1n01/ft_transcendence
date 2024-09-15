from django.db import models
from accounts.models import FtUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class FriendshipsStatusChoices(models.TextChoices):
    PENDING = "PENDING", _("pending")
    ACCEPTED = "ACCEPTED", _("accepted")
    BLOCKED = "BLOCKED", _("blocked")
    REMOVED = "REMOVED", _("removed")


class Friendships(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        FtUser,
        on_delete=models.CASCADE,
        verbose_name=_("ユーザー"),
        related_name="user",
    )
    friend = models.ForeignKey(
        FtUser,
        on_delete=models.CASCADE,
        verbose_name=_("フレンド"),
        related_name="friend",
    )
    status = models.CharField(
        verbose_name=_("状態"),
        max_length=10,
        choices=FriendshipsStatusChoices,
        default=FriendshipsStatusChoices.PENDING,
    )
    created_at = models.DateTimeField(
        verbose_name=_("作成日時"),
        null=True,
        blank=False,
    )
    updated_at = models.DateTimeField(verbose_name=_("変更日時"), auto_now=True)

    def __str__(self):
        return f"user={self.user.username}, friend={self.friend.username}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "friend"], name="friendship_unique"
            ),
        ]
