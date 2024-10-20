"""
URL configuration for ft_trans project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static


# import spa.urls
import accounts.urls
import users.urls
import friend.urls
import notification.urls
import pong.urls
import tournament.urls
import history.urls


# API
urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    # path("login/", include(login.urls)),
    path("i18n/", include("django.conf.urls.i18n")),
    # path("users/", include(users.urls), name="users"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("notification/", include(notification.urls), name="notification"),
    path("accounts/", include(accounts.urls), name="accounts"),
    path("pong/", include(pong.urls), name="pong"),
    path("tournament/", include(tournament.urls), name="tournament"),
    path("friend/", include(friend.urls), name="friend"),
    path("spa/", include(("spa.urls", "spa"), namespace="spa2")),
    path("users/", include(users.urls), name="users"),
    path("history/", include(history.urls), name="history"),
    path("", include(("spa.urls", "spa"), namespace="blank")),
    re_path(r"[\w\-\/]*", include(("spa.urls", "spa"), namespace="spa")),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
