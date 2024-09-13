from django.db import models
from accounts.models import FtUser
from django.utils.translation import gettext_lazy as _


class Tournament(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name=_("トーナメント名"), max_length=16)
    organizer = models.ForeignKey(
        FtUser, on_delete=models.CASCADE, verbose_name=_("主催者")
    )
    start_at = models.DateTimeField(verbose_name=_("開始時間"))
    is_only_friend = models.BooleanField("フレンドのみ")
    current_players = models.IntegerField(verbose_name=_("最大参加人数"))

    def save(self, *args, **kwargs):
        if self.current_players < 4 or self.current_players > 32:
            raise ValueError("current_players must be between 4 and 32")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id={self.id}: {self.start_at} ({self.current_players} players)"


class TournamentParticipant(models.Model):
    id = models.BigAutoField(primary_key=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participant = models.ForeignKey(FtUser, on_delete=models.CASCADE)
    is_accept = models.BooleanField()


"""
シード(正確には不戦勝)の場合はplayer2がnull
試合不成立の場合はplayer1,2のスコアが共にblank
"""


class Match(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    player1 = models.ForeignKey(FtUser, on_delete=models.PROTECT, related_name="player1")
    player2 = models.ForeignKey(FtUser, on_delete=models.PROTECT, related_name="player2", null=True)
    player1_score = models.SmallIntegerField(null=True)
    player2_score = models.SmallIntegerField(null=True)

    def __str__(self):
        return (
            f"id={self.id}: {self.player1} vs {self.player2} "
            + f"(player1_score={self.player1_score}, player2_score={self.player2_score})"
        )
