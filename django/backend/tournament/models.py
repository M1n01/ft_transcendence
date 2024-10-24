from django.db import models
from accounts.models import FtUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid

PLAYERNAME_MAX_LEN = getattr(settings, "USERNAME_MAX_LEN", None)
TOURNAMENTNAME_MAX_LEN = getattr(settings, "TOURNAMENTNAME_MAX_LEN", None)


class TournamentStatusChoices(models.TextChoices):
    RECRUITING = "RECRUITING", _("参加者募集中")
    ONGOING = "ONGOING", _("トーナメント進行中")
    ENDED = "ENDED", _("終了")
    CANCEL = "CANCEL", _("キャンセル")


class Tournament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        verbose_name=_("トーナメント名"), max_length=TOURNAMENTNAME_MAX_LEN
    )
    organizer = models.ForeignKey(
        FtUser,
        on_delete=models.PROTECT,
        verbose_name=_("主催者"),
        related_name="organizer",
    )
    start_at = models.DateTimeField(verbose_name=_("開始時間"))
    is_only_friend = models.BooleanField(verbose_name=_("フレンドのみ"), default=False)
    current_players = models.IntegerField(verbose_name=_("最大参加人数"))
    status = models.CharField(
        max_length=10,
        choices=TournamentStatusChoices,
        default=TournamentStatusChoices.RECRUITING,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organizer", "start_at"], name="tournament_unique"
            ),
        ]

    def save(self, *args, **kwargs):
        if self.current_players < 4 or self.current_players > 16:
            raise ValueError("current_players must be between 4 and 16")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id={self.id}: {self.start_at} ({self.current_players} players)"


class TournamentParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.PROTECT)
    participant = models.ForeignKey(FtUser, on_delete=models.PROTECT)
    alias_name = models.CharField(
        verbose_name=_("エイリアス名"), max_length=PLAYERNAME_MAX_LEN
    )
    is_accept = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tournament_id", "participant"],
                name="tournament_participant_unique",
            ),
        ]
