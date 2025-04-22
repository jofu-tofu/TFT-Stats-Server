from django.db import models
from django.contrib.postgres.fields import JSONField

class Player(models.Model):
    puuid = models.CharField(max_length=78, primary_key=True)
    summoner_id = models.CharField(max_length=63)
    region = models.CharField(max_length=5)
    tier = models.CharField(max_length=16, blank=True)
    rank = models.CharField(max_length=4, blank=True)
    league_points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

class Match(models.Model):
    match_id = models.CharField(max_length=32, primary_key=True)
    region = models.CharField(max_length=7)
    game_datetime = models.DateTimeField()
    patch = models.CharField(max_length=8)
    raw = JSONField()

class Participant(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="participants")
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    placement = models.PositiveSmallIntegerField()
    level = models.PositiveSmallIntegerField()
    traits = JSONField()
    units = JSONField()
    
    class Meta:
        indexes = [models.Index(fields=["placement", "level"])]
