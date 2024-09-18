from django.urls import path

# from django.views.generic import RedirectView
from tournament import views

# from views import Pong

app_name = "tournament"

urlpatterns = [
    path("", views.TournamentView.as_view(), name="tournament"),
    path(
        "recruiting/",
        views.RecruitingView.as_view(),
        name="recruiting",
    ),
    path(
        "organized/",
        views.OrganizedView.as_view(),
        name="organized",
    ),
    path(
        "participant/",
        views.ParticipantView.as_view(),
        name="participant",
    ),
    path(
        "register/",
        views.RegisterApi.as_view(),
        name="register",
    ),
]
# エンドユーザーによるファイルアップロードなどがある場合、
# それらを保持するディレクトリを定義する
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
# )
