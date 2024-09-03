from django.urls import path
from .views.score_keeper_views import SaveMatchScoreView

urlpatterns = [
    path("scores/", SaveMatchScoreView.as_view(), name="scores"),
]
