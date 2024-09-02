from django.urls import path, include
from .views.score_keeper_views import SaveMatchScoreView

urlpatterns = [
    path("scores/", SaveMatchScoreView.as_view(), name="scores"),
]
