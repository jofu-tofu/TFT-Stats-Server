"""
1.  Clone & split this file into the structure above.
2.  Create a `.env` with RIOT_API_KEY, POSTGRES_* creds, REDIS_URL.
3.  docker‑compose up  (sample compose file not included here)
4.  python manage.py migrate && python manage.py createsuperuser
5.  python manage.py ingest_puuid <some‑high‑elo‑player‑puuid> --region NA1
6.  celery -A tftstats worker -l info
7.  Browse /api/latest‑matches/ (wire up the URL in urls.py)
"""
