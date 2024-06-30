from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "account"

urlpatterns = [
    # path("admin/", admin.site.urls),
    # //path("accounts/", include("accounts.urls")),
    # path("/", views.Account.as_view(), name="account"),
    path("registration/login", views.LoginPage, name="login"),
    path("registration/logout", views.LogoutPage, name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("register/", views.UserRegistration.as_view(), name="register"),
    path("list/", views.UserList.as_view(), name="list"),
]
