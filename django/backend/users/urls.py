from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("edit-profile/", views.EditProfileView.as_view(), name="edit-profile"),
    path("delete-user", views.delete_user, name="delete-user"),
    path("privacy-policy/", views.PrivacyPolicy.as_view(), name="privacy-policy"),
    path("update-avatar/", views.UpdateAvatar.as_view(), name="update-avatar"),
]
