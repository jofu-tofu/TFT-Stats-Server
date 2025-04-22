from django.utils import timezone
from .models import Match, Participant, Player
from django.db import transaction


def ingest_match(raw: dict, region_cluster: str) -> Match:
    info = raw["info"]
    metadata = raw["metadata"]
    match_id = metadata["match_id"]
    defaults = {
        "region": region_cluster,
        "game_datetime": timezone.datetime.fromtimestamp(info["game_datetime"] / 1000, tz=timezone.utc),
        "patch": info.get("game_version", ""),
        "raw": raw,
    }
    match, created = Match.objects.update_or_create(match_id=match_id, defaults=defaults)

    if not created:
        return match  # already processed

    with transaction.atomic():
        for pdata in info["participants"]:
            p_obj, _ = Player.objects.get_or_create(puuid=pdata["puuid"], defaults={
                "region": pdata.get("region", "NA1"),
            })
            Participant.objects.create(
                match=match,
                puuid=p_obj,
                placement=pdata["placement"],
                level=pdata["level"],
                gold_left=pdata["gold_left"],
                last_round=pdata["last_round"],
                traits=pdata["traits"],
                units=pdata["units"],
            )
    return match