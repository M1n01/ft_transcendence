from rest_framework import serializers
from pong.models import Match


class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["tournament_id", "player1", "player1_score", "player2", "player2_score", "round"]


class MatchResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tournament_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    player1 = serializers.IntegerField()
    player1_score = serializers.IntegerField(allow_null=True)
    player2 = serializers.IntegerField(allow_null=True)
    player2_score = serializers.IntegerField(allow_null=True)
    round = serializers.IntegerField()
