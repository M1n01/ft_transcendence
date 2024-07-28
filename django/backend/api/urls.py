from django.urls import path, include

urlpatterns = [
    path("scorekeeper/", include("api.scorekeeper.urls")),
]
