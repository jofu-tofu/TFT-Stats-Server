from rest_framework import generics
from .models import Match
from .serializers import MatchSerializer

class LatestMatchesView(generics.ListAPIView):
    queryset = Match.objects.order_by("-game_datetime")[:100]
    serializer_class = MatchSerializer