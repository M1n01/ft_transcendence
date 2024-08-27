from rest_framework import serializers
from .models import Game


class GameRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["winner", "winner_score", "loser", "loser_score"]


class GameResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"
