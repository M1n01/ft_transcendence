from django.db import models


class Tournament(models.Model):
    id = models.BigAutoField(primary_key=True)
    max_players = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    current_players = models.IntegerField()


class Match(models.Model):
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    winner = models.IntegerField()
    loser = models.IntegerField(allow_null=True) # シード(不戦勝)の場合はnull
    winner_score = models.SmallIntegerField()
    loser_score = models.SmallIntegerField(allow_null=True)
    round = models.SmallIntegerField()

    def __str__(self):
        return f"id={self.id}: {self.winner} vs {self.loser} (winner_score={self.winner_score}, loser_score={self.loser_score})"
