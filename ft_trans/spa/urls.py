from django.urls import path, include
from . import views
import pong.urls

from django.views.generic import TemplateView

app_name = "spa"

urlpatterns = [
    # path('lang', views.lang, name='lang'),
    # path('/script', include(pong.urls)),
    # path('script2', views.script2, name='script2'),
    # path('pong', include(pong.urls)),
    # path("", views.index, name="index"),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
]
