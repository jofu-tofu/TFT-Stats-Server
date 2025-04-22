from django.core.management.base import BaseCommand
from tftstats.ingester.clients import get_match_ids, get_match, PLATFORM_CLUSTER
from tftstats.ingester.etl import ingest_match

class Command(BaseCommand):
    help = "Fetch recent matches for a PUUID"

    def add_arguments(self, parser):
        parser.add_argument("puuid")
        parser.add_argument("--region", default="NA1")
        parser.add_argument("--count", type=int, default=20)

    def handle(self, *a, **o):
        puuid, region, count = o["puuid"], o["region"], o["count"]
        cluster = PLATFORM_CLUSTER[region]
        for mid in get_match_ids(puuid, region, count):
            m = ingest_match(get_match(mid, cluster), cluster)
            self.stdout.write(f"✔ {m.match_id}")
