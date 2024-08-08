from rest_framework import serializers
from .models import Player, Score


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("player_id", "score")


class ScoreSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    opponent = PlayerSerializer()

    class Meta:
        model = Score
        fields = ("match_id", "player", "opponent")
