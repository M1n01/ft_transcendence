from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from pong import views

# from views import Pong

app_name = "pong"

urlpatterns = [
    path("lang", views.lang, name="lang"),
    path("script", views.script, name="script"),
    path("script2", views.script2, name="script2"),
    path("test", views.test),
    path("index", views.index),
    path("", views.index),
]
# エンドユーザーによるファイルアップロードなどがある場合、
# それらを保持するディレクトリを定義する
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
# )
