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
    path("tournament", views.TournamentView.as_view(), name="tournament"),
    path("tournament-chart", views.TournamentView.as_view(), name="tournament-chart"),
    path("games", views.GamesView.as_view(), name="games"),
    path(
        "register-tournament",
        views.RegisterTournament.as_view(),
        name="register-tournament",
    ),
    path("", RedirectView.as_view(url="/games")),
]
# エンドユーザーによるファイルアップロードなどがある場合、
# それらを保持するディレクトリを定義する
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
# )
