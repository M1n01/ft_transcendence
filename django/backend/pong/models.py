from django.db import models


class Tournament(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    current_players = models.IntegerField(min_value=4, max_value=32)


'''
シード(正確には不戦勝)の場合はplayer2がnull
試合不成立の場合はplayer1,2のスコアが共に0
'''
class Match(models.Model):
    id = models.BigAutoField(primary_key=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    player1 = models.IntegerField()
    player2 = models.IntegerField(allow_null=True) # シード(不戦勝)の場合はnull
    player1_score = models.SmallIntegerField()
    player2_score = models.SmallIntegerField(allow_null=True)

    def __str__(self):
        return f"id={self.id}: {self.winner} vs {self.loser} (winner_score={self.winner_score}, loser_score={self.loser_score})"
