from django.db import models


class Player(models.Model):
    player_id = models.IntegerField()
    score = models.IntegerField()


class Score(models.Model):
    match_id = models.IntegerField()
    player = models.ForeignKey(Player, related_name="player", on_delete=models.CASCADE)
    opponent = models.ForeignKey(
        Player, related_name="opponent", on_delete=models.CASCADE
    )
