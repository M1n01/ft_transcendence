from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("edit-profile/", views.EditProfileView.as_view(), name="edit-profile"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path(
        "changed-password/",
        views.ChangedPasswordView.as_view(),
        name="changed-password",
    ),
    path("delete-user/", views.DeleteUserView.as_view(), name="delete-user"),
    path("privacy-policy/", views.PrivacyPolicy.as_view(), name="privacy-policy"),
    path("update-avatar/", views.UpdateAvatar.as_view(), name="update-avatar"),
]
