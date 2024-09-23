# from django.contrib import admin
from django.urls import path
from . import views

app_name = "friend"

urlpatterns = [
    path("request/", views.FriendRequest.as_view(), name="request"),
    path("respond/", views.RespondFriendRequest.as_view(), name="respond"),
    path("", views.FriendView.as_view(), name="friend"),
]
