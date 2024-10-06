# from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from users import views

app_name = "users"

urlpatterns = [
    path("test", views.test, name="test"),
    path("profile", views.profile, name="profile"),
    path("edit-profile", views.edit_profile, name="edit-profile"),
    path("delete-user", views.delete_user, name="delete-user"),
    path("privacy-policy", views.privacy_policy, name="privacy-policy"),
]
