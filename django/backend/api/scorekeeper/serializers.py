from rest_framework import serializers
from .models import Match, Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["player_id", "score"]


class MatchSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    opponent = PlayerSerializer()

    class Meta:
        model = Match
        fields = ["match_id", "player", "opponent"]

    def create(self, validated_data):
        player_data = validated_data.pop("player")
        opponent_data = validated_data.pop("opponent")

        player = Player.objects.create(**player_data)
        opponent = Player.objects.create(**opponent_data)

        match = Match.objects.create(player=player, opponent=opponent, **validated_data)
        return match
