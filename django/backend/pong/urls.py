from django.urls import path
from django.views.generic import RedirectView
from pong import views

# from views import Pong

app_name = "pong"

urlpatterns = [
    path("lang", views.lang, name="lang"),
    path("script", views.script, name="script"),
    path("script2", views.script2, name="script2"),
    path("test", views.test),
    path("index", views.index),
    path("", RedirectView.as_view(url="/games")),
    path("games", views.GamesView.as_view(), name="games"),
    path("start", views.StartPong.as_view(), name="start"),
    path(
        "tournament-detail", views.TournamentDetail.as_view(), name="tournament-detail"
    ),
    path("add-score/<uuid:pk>", views.AddScore.as_view(), name="add-score"),
    path("matches/<uuid:pk>", views.MatchView.as_view(), name="match"),
]
