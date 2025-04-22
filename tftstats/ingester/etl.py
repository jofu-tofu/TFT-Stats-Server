from django.db import transaction
from django.utils import timezone
from tftstats.matches.models import Player, Match, Participant

def ingest_match(raw: dict, cluster: str) -> Match:
    info, meta = raw["info"], raw["metadata"]
    match_id = meta["match_id"]
    match, created = Match.objects.get_or_create(
        match_id=match_id,
        defaults={
            "region": cluster,
            "game_datetime": timezone.datetime.fromtimestamp(info["game_datetime"] / 1000, tz=timezone.utc),
            "patch": info.get("game_version", ""),
            "raw": raw
        },
    )
    if not created:
        return match

    with transaction.atomic():
        for p in info["participants"]:
            player, _ = Player.objects.get_or_create(
                puuid=p["puuid"],
                defaults={"region": p.get("region", "NA1")}
            )
            Participant.objects.create(
                match=match,
                player=player,
                placement=p["placement"],
                level=p["level"],
                traits=p["traits"],
                units=p["units"]
            )
    return match
