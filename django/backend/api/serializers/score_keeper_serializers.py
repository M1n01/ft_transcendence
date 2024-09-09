from rest_framework import serializers
from ...pong.models import Match


class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["tournament_id", "round", "player1", "player1_score", "player2", "player2_score"]


class MatchResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"
