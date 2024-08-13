from django.db import models

from accounts.models import FtUser


class Game(models.Model):
    id = models.BigAutoField(primary_key=True)
    winner = models.ForeignKey(
        FtUser, related_name="game_winner", on_delete=models.CASCADE
    )
    loser = models.ForeignKey(
        FtUser, related_name="game_loser", on_delete=models.CASCADE
    )
    winner_score = models.SmallIntegerField()
    loser_score = models.SmallIntegerField()

    def __str__(self):
        return f"id={self.id}: {self.winner} vs {self.loser}"
