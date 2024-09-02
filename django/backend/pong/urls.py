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
    path("tournament", views.TournamentView.as_view(), name="games"),
    path("games", views.GamesView.as_view(), name="games"),
    path("", RedirectView.as_view(url="/games")),
]
# エンドユーザーによるファイルアップロードなどがある場合、
# それらを保持するディレクトリを定義する
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
# )
