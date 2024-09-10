from django.db import models


class Tournament(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_at = models.DateTimeField()
    current_players = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.current_players < 4 or self.current_players > 32:
            raise ValueError("current_players must be between 4 and 32")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id={self.id}: {self.start_at} ({self.current_players} players)"


"""
シード(正確には不戦勝)の場合はplayer2がnull
試合不成立の場合はplayer1,2のスコアが共にblank
"""


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
        return f"id={self.id}: {self.player1} vs {self.player2} (player1_score={self.player1_score}, player2_score={self.player2_score})"
