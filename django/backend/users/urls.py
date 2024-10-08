# from django.contrib import admin
from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("test", views.test, name="test"),
    path("profile/", views.Profile.as_view(), name="profile"),
    path("edit-profile/", views.edit_profile, name="edit-profile"),
    path("delete-user", views.delete_user, name="delete-user"),
    path("privacy-policy/", views.privacy_policy, name="privacy-policy"),
    path("update-avatar/", views.UpdateAvatar.as_view(), name="update-avatar"),
]
