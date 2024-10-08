# from django.contrib import admin
from django.urls import path
from . import views

app_name = "history"

urlpatterns = [
    path("", views.History.as_view(), name="history"),
    path(
        "ovo/",
        views.OVOMatch.as_view(),
        name="ovo",
    ),
    path(
        "tournament/",
        views.TournamentMatch.as_view(),
        name="tournament",
    ),
]
