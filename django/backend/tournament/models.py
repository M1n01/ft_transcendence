from django.db import models
from accounts.models import FtUser
from django.utils.translation import gettext_lazy as _


class TournamentStatusChoices(models.TextChoices):
    RECRUITING = "RECRUITING", _("参加者募集中")
    ONGOING = "ONGOING", _("トーナメント進行中")
    ENDED = "ENDED", _("終了")
    CANCEL = "CANCEL", _("キャンセル")


class Tournament(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name=_("トーナメント名"), max_length=32)
    organizer = models.ForeignKey(
        FtUser, on_delete=models.CASCADE, verbose_name=_("主催者")
    )
    start_at = models.DateTimeField(verbose_name=_("開始時間"))
    is_only_friend = models.BooleanField(verbose_name=_("フレンドのみ"), default=False)
    current_players = models.IntegerField(verbose_name=_("最大参加人数"))
    status = models.CharField(
        max_length=10,
        choices=TournamentStatusChoices,
        default=TournamentStatusChoices.RECRUITING,
    )

    def save(self, *args, **kwargs):
        if self.current_players < 4 or self.current_players > 32:
            raise ValueError("current_players must be between 4 and 32")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id={self.id}: {self.start_at} ({self.current_players} players)"


class TournamentParticipant(models.Model):
    id = models.BigAutoField(primary_key=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participant = models.ForeignKey(FtUser, on_delete=models.CASCADE)
    alias_name = models.CharField(verbose_name=_("エイリアス名"), max_length=32)
    is_accept = models.BooleanField(default=False)
