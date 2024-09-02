from django.db import models


class Game(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    winner = models.IntegerField()
    loser = models.IntegerField()
    winner_score = models.SmallIntegerField()
    loser_score = models.SmallIntegerField()

    def __str__(self):
        return f"id={self.id}: {self.winner} vs {self.loser}"
