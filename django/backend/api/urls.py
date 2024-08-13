from django.urls import path, include
from .views import SaveGameScoreView

urlpatterns = [
    path("scores/", SaveGameScoreView.as_view(), name="scores"),
]
