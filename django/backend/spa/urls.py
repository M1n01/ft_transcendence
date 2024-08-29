from django.urls import path
from . import views


app_name = "spa"

urlpatterns = [
    path("top", views.Top.as_view(), name="top"),
    path("nav", views.Nav.as_view(), name="nav"),
    path("", views.Index.as_view(), name="index"),
]
