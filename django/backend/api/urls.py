from django.urls import path, include
from .views import SaveMatchScoreView

urlpatterns = [
    path("scores/", SaveMatchScoreView.as_view(), name="scores"),
]
