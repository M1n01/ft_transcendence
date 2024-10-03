import spa.urls
from tournament import views
from django.urls import include, path, re_path

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
        "all/",
        views.AllView.as_view(),
        name="all",
    ),
    path(
        "register/",
        views.RegisterApi.as_view(),
        name="register",
    ),
    path(
        "details/<int:pk>",
        views.DetailView.as_view(),
        name="details",
    ),
    path(
        "info/<int:pk>",
        views.InfoApi.as_view(),
        name="info",
    ),
    re_path(r"[\w\-\/]*", include(spa.urls), name="error"),
]
# エンドユーザーによるファイルアップロードなどがある場合、
# それらを保持するディレクトリを定義する
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
# )
