from rest_framework import serializers
from .models import Participant, Match

class UnitSerializer(serializers.Serializer):
    character_id = serializers.CharField()
    tier = serializers.IntegerField()
    items = serializers.ListField(child=serializers.IntegerField())

class ParticipantSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True)
    class Meta:
        model = Participant
        fields = ("placement", "level", "gold_left", "units", "traits")

class MatchSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, source="participants")
    class Meta:
        model = Match
        fields = ("match_id", "patch", "game_datetime", "participants")