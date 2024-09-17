from django.shortcuts import render
from django.db import models
from django.http import Http404
from django.views.decorators.http import condition
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
import hashlib

from .models import Tournament, TournamentParticipant, TournamentStatusChoices
from .forms import TournamentForm
from django.views.generic.edit import UpdateView

from django.http import (
    # JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    # HttpResponseForbidden,
    HttpResponse,
)
from django.urls import reverse_lazy


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


class RegisterTournament(UpdateView):
    model = Tournament
    fields = ["id", "status"]
    template_name = "pong/tournament-register.html"  # 使わない
    success_url = reverse_lazy("pong:tournament")
    # queryset = Friendships.objects.all()

    def get(self, request):
        print("register No.1")
        return HttpResponse()

    def post(self, request):
        id = request.POST.get("id")
        # status = request.POST.get("status")
        tournament = Tournament.objects.get(id=id)
        TournamentParticipant.objects.create(
            tournament_id=tournament, participant=request.user, is_accept=True
        )
        return HttpResponse()

    def form_valid(self, form):
        print("register No.6")

        print("respond No.1")
        # モデルを保存する
        try:
            print("respond No.2")
            print("register No.7")
            form.save()
            print("respond No.3")
        except Exception:
            print("respond No.4")
            return HttpResponseServerError()
        print("respond No.5")
        return HttpResponse()

    def form_invalid(self, form):
        print("register No.8")
        return HttpResponseBadRequest()

    pass


# class TournamentView(TemplateView):
class TournamentView(LoginRequiredMixin, CreateView):
    # model = Tournament
    # form = TournamentForm
    form_class = TournamentForm
    template_name = "pong/tournament.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["as_organizer"] = Tournament.objects.filter(organizer=self.request.user)
        context["as_participant"] = TournamentParticipant.objects.filter(
            participant=self.request.user, is_accept=True
        )
        tmp_tournaments = context["as_participant"].values_list(
            "tournament_id", flat=True
        )
        context["recruiting_tournaments"] = Tournament.objects.exclude(
            id__in=tmp_tournaments
        ).filter(status=TournamentStatusChoices.RECRUITING.value)

        return context

    def post(self, request):
        form = TournamentForm(self.request.POST)
        form.set_organizer(request.user)
        # form.set_only_user(self.request.POST.get("is_only_friend"))
        # tmp_res = super().form_valid(form)

        name = self.request.POST.get("name")
        start_at = self.request.POST.get("start_at")
        current_players = int(self.request.POST.get("current_players"))
        is_only_friend = (
            True if self.request.POST.get("is_only_friend") == "on" else False
        )
        organizer = request.user
        Tournament.objects.create(
            name=name,
            organizer=organizer,
            start_at=start_at,
            is_only_friend=is_only_friend,
            current_players=current_players,
        )
        return HttpResponse()
