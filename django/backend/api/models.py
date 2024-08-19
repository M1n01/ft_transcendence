from django.db import models

from accounts.models import FtUser


class Game(models.Model):
    id = models.BigAutoField(primary_key=True)
    winner = models.IntegerField()
    loser = models.IntegerField()
    winner_score = models.SmallIntegerField()
    loser_score = models.SmallIntegerField()

    def __str__(self):
        return f"id={self.id}: {self.winner} vs {self.loser}"
