from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.db import models
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.http import Http404
from urllib.parse import urlparse
from django.template import RequestContext, Template
from django.views.decorators.http import condition
import django.views.decorators.http
import asyncio
import hashlib
from django.conf import settings


def checkSPA(request):
    spa = request.META.get("HTTP_SPA")
    spas = request.META.get("HTTPS_SPA")
    if spa is None and spas is None:
        Http404("not allowed")
    if spa and spa == "spa":
        return True
    if spas and spas == "spa":
        return True
    Http404("not allowed")
    return False


# Create your views here.
class Pong(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


def my_etag(request, *args, **kwargs):
    return hashlib.md5(
        ":".join(request.GET.dict().values()).encode("utf-8")
    ).hexdigest()


# テスト用　後で消す
@condition(etag_func=my_etag)
def lang(request):
    return render(request, "pong/lang_test.html")


@condition(etag_func=my_etag)
def script(request):
    checkSPA(request)
    return render(request, "pong/script.html")


@condition(etag_func=my_etag)
def script2(request):
    return render(request, "pong/script2.html")


@condition(etag_func=my_etag)
def test(request):
    return render(request, "pong/test.html")


@condition(etag_func=my_etag)
def index(request):
    context = {
        "latest_question_list": "abcdefg",
    }
    return render(request, "pong/index.html", context)
