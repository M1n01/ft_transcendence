from django.urls import path, include
from .views import ScoreAPIView

urlpatterns = [
    path("scores/", ScoreAPIView.as_view(), name="scores"),
]
