from celery import shared_task
from . import api, services, constants as C

@shared_task(bind=True, max_retries=3)
def fetch_and_ingest_matches(self, region: str = "NA1") -> int:
    try:
        puuids = api.get_challenger_players(region)
        cluster = api.PLATFORM_CLUSTER[region]
        ingested = 0
        for puuid in puuids:
            match_ids = api.get_match_ids(puuid, region)
            for mid in match_ids:
                raw = api.get_match(mid, cluster)
                services.ingest_match(raw, cluster)
                ingested += 1
        return ingested
    except Exception as exc:
        raise self.retry(exc=exc, countdown=30)