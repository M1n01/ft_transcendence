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
from django.urls import path
from django.urls import include, path, re_path
from django.conf.urls.i18n import i18n_patterns
import pong.urls

import spa.urls
import accounts.urls


# API
urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api/', include(api.urls)),
    # path("login/", include(login.urls)),
    path("accounts/", include(accounts.urls)),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("pong/", include(pong.urls)),
    re_path(r"[\w\-\/]*", include(spa.urls)),
    prefix_default_language=True,
)
