from django.urls import path
from .views import LatestMatchesView

urlpatterns = [
    path('latest-matches/', LatestMatchesView.as_view(), name='latest-matches'),
]
