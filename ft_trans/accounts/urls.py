from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    # path("registration/login", views.LoginPage, name="login"),
    # path("registration/logout", views.LogoutPage, name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    #    path("list/", views.UserList.as_view(), name="list"),
    path("success-signup/", views.SignupSuccess, name="success-signup"),
    path("success-login/", views.LoginSuccess, name="success-login"),
    path("success-logout/", views.LogoutSuccess, name="success-logout"),
    path("list/", views.UserList.as_view(), name="list"),
    # path("list/", views.SignupSuccess, name="list"),
]
