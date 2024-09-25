from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup-tmp/", views.SignupView.as_view(), name="signup-tmp"),
    path("signup-two-fa/", views.signup_two_fa_verify, name="signup-two-fa"),
    path("login-tmp/", views.UserLogin.as_view(), name="login-tmp"),
    path("two-fa/", views.TwoFAView.as_view(), name="two-fa"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("redirect-oauth", views.redirect_oauth, name="redirect-oauth"),
    path("oauth-login", views.oauth_login, name="oauth-login"),
    path("login-signup/", views.LoginSignupView.as_view(), name="login-signup"),
]
