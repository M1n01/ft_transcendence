from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.db import models
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django.http import Http404
from urllib.parse import urlparse

def checkSPA(request):
    spa = request.META.get('HTTP_SPA')
    spas = request.META.get('HTTPS_SPA')
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

# テスト用　後で消す
def lang(request):
    return render(request, 'pong/lang_test.html')

def script(request):
    checkSPA(request)
    return render(request, 'pong/script.html')


def script2(request):
    return render(request, 'pong/script2.html')


def test(request):
    return render(request, 'pong/test.html')


def index(request):
    context = {
        "latest_question_list": "abcdefg",
    }
    return render(request, "pong/index.html", context)