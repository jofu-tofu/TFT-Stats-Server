from celery import shared_task
from tftstats.ingester.clients import get_challenger_players, get_match_ids, get_match, PLATFORM_CLUSTER
from tftstats.ingester.etl import ingest_match

@shared_task(bind=True, max_retries=3)
def fetch_and_ingest_matches(self, region="NA1"):
    try:
        puuids = get_challenger_players(region)
        cluster = PLATFORM_CLUSTER[region]
        n = 0
        for puuid in puuids:
            for mid in get_match_ids(puuid, region):
                ingest_match(get_match(mid, cluster), cluster)
                n += 1
        return n
    except Exception as e:
        raise self.retry(exc=e, countdown=30)
