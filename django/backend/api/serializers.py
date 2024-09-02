from rest_framework import serializers
from .models import Match


class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["winner", "winner_score", "loser", "loser_score"]


class MatchResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"
