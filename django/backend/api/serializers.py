from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    player_id = serializers.IntegerField()
    score = serializers.IntegerField()


class ScoreSerializer(serializers.ModelSerializer):
    match_id = serializers.IntegerField()
    player = PlayerSerializer()
    opponent = PlayerSerializer()
