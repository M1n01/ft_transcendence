from django.db import models


class Match(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    winner = models.IntegerField()
    loser = models.IntegerField()
    winner_score = models.SmallIntegerField()
    loser_score = models.SmallIntegerField()

    def __str__(self):
        return f"id={self.id}: {self.winner} vs {self.loser} (winner_score={self.winner_score}, loser_score={self.loser_score})"
