from django.db import models


class Player(models.Model):
    player_id = models.IntegerField()
    score = models.IntegerField()


class Match(models.Model):
    match_id = models.CharField(max_length=255)
    player = models.ForeignKey(Player, related_name="player", on_delete=models.CASCADE)
    opponent = models.ForeignKey(
        Player, related_name="opponent", on_delete=models.CASCADE
    )
