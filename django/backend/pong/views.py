from django.shortcuts import render
from django.db import models
from django.http import Http404
from django.views.decorators.http import condition
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
import hashlib

from .models import Tournament
from .forms import TournamentForm


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
class Pong(models.Model, LoginRequiredMixin):
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


def script_view(request):
    checkSPA(request)
    return render(request, "pong/script.html")


# @condition(etag_func=my_etag)
def script(request):
    # script_view(request)
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


class GamesView(TemplateView):
    template_name = "pong/games.html"


class TournamentListView(ListView):
    model = Tournament
    template_name = "pong/tournament-list.html"
    context_object_name = "notifications"
    paginate_by = 10

    def get_queryset(self):
        return Tournament.objects.order_by("start_at").reverse().first()


# class TournamentView(TemplateView):
class TournamentView(LoginRequiredMixin, CreateView):
    # model = Tournament
    # form = TournamentForm
    form_class = TournamentForm
    template_name = "pong/tournament.html"

    def post(request):
        print("post")
