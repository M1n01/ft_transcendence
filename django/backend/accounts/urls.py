# from django.contrib import admin
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # path("signup/", views.SignupView.as_view(), name="signup"),
    path("signup-valid/", views.SignupView.as_view(), name="signup-valid"),
    # path("signup-valid/", views.signup_valid, name="signup-valid"),
    path("signup-tmp/", views.SignupTmpView.as_view(), name="signup-tmp"),
    path("signup-two-fa/", views.signup_two_fa, name="signup-two-fa"),
    path(
        "signup-two-fa-verify/", views.signup_two_fa_verify, name="signup-two-fa-verify"
    ),
    path("two-fa-verify/", views.two_fa_verify, name="two-fa-verify"),
    path("send-two-fa/", views.send_two_fa_view, name="send-two-fa"),
    # path("signup-valid/", views.signup_valid, name="signup-valid"),
    path("login/", views.UserLogin.as_view(), name="login"),
    # path("login-tmp/", views.UserTmpLogin.as_view(), name="login-tmp"),
    path("login-tmp/", views.UserLogin.as_view(), name="login-tmp"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("success-signup/", views.SignupSuccess, name="success-signup"),
    path("success-login/", views.LoginSuccess, name="success-login"),
    path("success-logout/", views.LogoutSuccess, name="success-logout"),
    path("redirect-oauth/", views.redirect_oauth, name="redirect-oauth"),
    path("oauth-login/", views.oauth_login, name="oauth-login"),
    # path("signup-two-fa/", views.signup_two_fa, name="signup-two-fa"),
    path("two-fa/", views.two_fa, name="two-fa"),
    path("two-fa-verify/", views.two_fa_verify, name="two-fa-verify"),
    path("login-signup/", views.LoginSignupView.as_view(), name="login-signup"),
]
