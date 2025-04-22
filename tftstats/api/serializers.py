from rest_framework import serializers
from tftstats.matches.models import Match, Participant

class UnitSerializer(serializers.Serializer):
    character_id = serializers.CharField()
    tier = serializers.IntegerField()
    items = serializers.ListField(child=serializers.IntegerField())

class ParticipantSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True)
    class Meta:
        model = Participant
        fields = ("placement", "level", "units", "traits")

class MatchSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(source="participants", many=True)
    class Meta:
        model = Match
        fields = ("match_id", "patch", "game_datetime", "participants")
