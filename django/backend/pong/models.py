from django.db import models

# from accounts.models import FtUser
# from django.utils.translation import gettext_lazy as _
from tournament.models import Tournament
from accounts.models import FtUser


class Match(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    player1 = models.IntegerField()
    player2 = models.IntegerField(null=True)  # シード(不戦勝)の場合はnull
    player1_score = models.SmallIntegerField(null=True)
    player2_score = models.SmallIntegerField(null=True)

    def __str__(self):
        return (
            f"id={self.id}: {self.player1} vs {self.player2} "
            + f"(player1_score={self.player1_score}, player2_score={self.player2_score})"
        )


class MatchTmp(models.Model):
    """
    Matchと内容はほぼ同じ
    BlockChainではなく、DBに保持する一時データ
    """

    id = models.BigAutoField(primary_key=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True)
    round = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    player1 = models.ForeignKey(
        FtUser, on_delete=models.SET_NULL, null=True, related_name="player1"
    )
    player2 = models.ForeignKey(
        FtUser, on_delete=models.SET_NULL, null=True, related_name="player2"
    )
    player1_score = models.SmallIntegerField(default=0)
    player2_score = models.SmallIntegerField(default=0)

    def __str__(self):
        return (
            f"id={self.id}:{self.round=} {self.player1} vs {self.player2} "
            + f"(player1_score={self.player1_score}, player2_score={self.player2_score})"
        )
