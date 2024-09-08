from rest_framework import serializers
from ...pong.models import Match


class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["winner", "winner_score", "loser", "loser_score"]


class MatchResponseSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = Match
        fields = "__all__"
