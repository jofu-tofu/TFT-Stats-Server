SET_NUMBER: int = 14        # ← placeholder – update every set
PATCH_VERSION: str = "14.8" # ← keep in sync with live balance patch
REGIONS: tuple[str, ...] = (
    "BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "NA1", "OC1",
    "PH2", "SG2", "TH2", "TR1", "TW2", "VN2",
)
QUEUE_ID_RANKED: int = 1100  # TFT ranked queue
MAX_MATCHES_PER_PUUID: int = 20  # safety cap per ingest run
RATE_LIMIT_RETRY: int = 2    # seconds to wait on HTTP 429 before retrying