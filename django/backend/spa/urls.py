from django.urls import path
from . import views


app_name = "spa"

urlpatterns = [
    path("top", views.Top.as_view(), name="top"),
    path("nav", views.Nav.as_view(), name="nav"),
    path("is-login", views.isLogin.as_view(), name="is-login"),
    path("to-login", views.ToLogin.as_view(), name="to-login"),
    path("", views.Index.as_view(), name="index"),
]
