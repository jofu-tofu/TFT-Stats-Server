from __future__ import annotations
import os, time, logging, requests
from typing import Any, Sequence
from tftstats import constants as C

log = logging.getLogger(__name__)

_API_KEY = os.environ["RIOT_API_KEY"]
HEADERS = {"X-Riot-Token": _API_KEY, "User-Agent": "TFTStats/1.0"}

REGION_HOST = {
    "AMERICAS": "https://americas.api.riotgames.com",
    "EUROPE": "https://europe.api.riotgames.com",
    "ASIA": "https://asia.api.riotgames.com"
}

PLATFORM_CLUSTER = {
    "NA1": "AMERICAS",
    "BR1": "AMERICAS",
    "LA1": "AMERICAS",
    "LA2": "AMERICAS",
    "OC1": "AMERICAS",
    "EUN1": "EUROPE",
    "EUW1": "EUROPE",
    "TR1": "EUROPE",
    "RU": "EUROPE",
    "KR": "ASIA",
    "JP1": "ASIA"
}

session = requests.Session()
session.headers.update(HEADERS)

class RiotAPIError(Exception):
    ...

def _request(url: str, params: dict[str, Any] | None = None) -> Any:
    for attempt in range(5):
        r = session.get(url, params=params, timeout=5)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", C.RATE_LIMIT_RETRY)))
            continue
        if 500 <= r.status_code < 600:
            time.sleep(1 + attempt)
            continue
        if r.ok:
            return r.json()
        raise RiotAPIError(f"{r.status_code}:{r.text}")
    raise RiotAPIError("max retries")

def get_challenger_players(region: str) -> Sequence[str]:
    url = f"https://{region.lower()}.api.riotgames.com/tft/league/v1/challenger"
    data = _request(url)
    return [e["puuid"] for e in data.get("entries", [])]

def get_match_ids(puuid: str, region: str, count: int = C.MAX_MATCHES_PER_PUUID) -> list[str]:
    cluster = PLATFORM_CLUSTER[region]
    url = f"{REGION_HOST[cluster]}/tft/match/v1/matches/by-puuid/{puuid}/ids"
    return _request(url, {"count": count})

def get_match(match_id: str, cluster: str) -> dict[str, Any]:
    url = f"{REGION_HOST[cluster]}/tft/match/v1/matches/{match_id}"
    return _request(url)
