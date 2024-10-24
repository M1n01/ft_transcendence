from django.db import models
from accounts.models import FtUser
from django.utils.translation import gettext_lazy as _
import uuid


# Create your models here.
class FriendshipsStatusChoices(models.TextChoices):
    PENDING = "PENDING", _("pending")
    ACCEPTED = "ACCEPTED", _("accepted")
    BLOCK = "BLOCK", _("block")  # ブロックする時
    BLOCKED = "BLOCKED", _("blocked")  # ブロックされた時
    # REMOVED = "REMOVED", _("removed") # 削除で対応する


class Friendships(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        FtUser,
        on_delete=models.CASCADE,
        verbose_name=_("ユーザー"),
        related_name="Friendships_user",
    )
    friend = models.ForeignKey(
        FtUser,
        on_delete=models.CASCADE,
        verbose_name=_("フレンド"),
        related_name="Friendships_friend",
    )
    message = models.CharField(
        verbose_name=_("メッセージ"),
        max_length=200,
        null=True,
        blank=True,
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
        auto_now_add=True,
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
