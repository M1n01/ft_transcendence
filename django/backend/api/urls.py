from django.urls import path, include
from .views import ScoreAPIView

api_patterns = [
    # ここにapiのパスを追加していく
    path("scores/", ScoreAPIView.as_view()),
]

urlpatterns = [
    path("api/", include(api_patterns)),
]
