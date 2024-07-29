from rest_framework import serializers
from .models import Match, Player


class PlayerSerializer(serializers.ModelSerializer):
    player_id = serializers.IntegerField()
    score = serializers.IntegerField()


class MatchSerializer(serializers.ModelSerializer):
    match_id = serializers.IntegerField()
    player = PlayerSerializer()
    opponent = PlayerSerializer()
