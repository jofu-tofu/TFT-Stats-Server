# TFT Stats Server

### Run locally
$ cp .env.example .env  # fill secrets
$ docker-compose up -d --build
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser  # optional
$ docker-compose exec web python manage.py ingest_puuid <PUUID> --region NA1

Browse http://localhost:8000/api/latest-matches/

### Shutdown
$ docker-compose down        # keep volumes
$ docker-compose down -v     # nuke db & redis data

