from django.core.management.base import BaseCommand
from stats import api, services

class Command(BaseCommand):
    help = "Fetches recent matches for a given PUUID and ingests them into the DB"

    def add_arguments(self, parser):
        parser.add_argument("puuid", type=str)
        parser.add_argument("--region", default="NA1")
        parser.add_argument("--count", type=int, default=20)

    def handle(self, *args, **opts):
        puuid = opts["puuid"]
        region = opts["region"]
        count = opts["count"]
        cluster = api.PLATFORM_CLUSTER[region]
        self.stdout.write(f"Fetching {count} matches for {puuid}…")
        for mid in api.get_match_ids(puuid, region, count):
            raw = api.get_match(mid, cluster)
            match = services.ingest_match(raw, cluster)
            self.stdout.write(f"✔  {match.match_id}")