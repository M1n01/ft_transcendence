# from django.shortcuts import render
# from django.db import models
# from django.http import Http404
# from django.views.decorators.http import condition
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView

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
from django.utils.translation import gettext_lazy as _
import re


class RecruitingView(ListView):
    model = Tournament
    template_name = "tournament/list.html"
    context_object_name = "tournaments"
    paginate_by = 9

    def get_queryset(self):
        return Tournament.objects.filter(
            status=TournamentStatusChoices.RECRUITING.value
        ).order_by("-start_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("登録可能トーナメント")
        return context


class OrganizedView(ListView):
    model = Tournament
    template_name = "tournament/list.html"
    context_object_name = "tournaments"
    paginate_by = 9

    def get_queryset(self):
        return Tournament.objects.filter(organizer=self.request.user).order_by(
            "-start_at"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("主催したトーナメント")
        return context


class ParticipantView(ListView):
    model = Tournament
    template_name = "tournament/list.html"
    context_object_name = "tournaments"
    paginate_by = 9

    def get_queryset(self):
        tmp_participant = TournamentParticipant.objects.filter(
            participant=self.request.user, is_accept=True
        )
        tmp_participant_tournaments = tmp_participant.values_list(
            "tournament_id", flat=True
        )

        return Tournament.objects.filter(id__in=tmp_participant_tournaments).order_by(
            "-start_at"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("登録済みトーナメント")
        return context


# class TournamentListView(ListView):
#    model = Tournament
#    template_name = "pong/list.html"
#    context_object_name = "notifications"
#    paginate_by = 10
#
#    def get_queryset(self):
#        return Tournament.objects.order_by("start_at").reverse().first()


class RegisterApi(UpdateView):
    model = Tournament
    fields = ["id", "status"]
    template_name = "tournament/register.html"  # 使わない
    success_url = reverse_lazy("tournament:tournament")
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
    template_name = "tournament/tournament.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["as_organizer"] = Tournament.objects.filter(
            organizer=self.request.user
        ).order_by("-start_at")[:4]
        tmp_participant = TournamentParticipant.objects.filter(
            participant=self.request.user, is_accept=True
        )
        tmp_participant_tournaments = tmp_participant.values_list(
            "tournament_id", flat=True
        )

        # context["as_participant"] = Tournament.objects.filter(
        # organizer=self.request.user
        # )

        context["as_participant"] = Tournament.objects.filter(
            id__in=tmp_participant_tournaments
        ).order_by("-start_at")[:4]

        context["recruiting"] = (
            Tournament.objects.exclude(id__in=tmp_participant_tournaments)
            .filter(status=TournamentStatusChoices.RECRUITING.value)
            .order_by("-start_at")
        )[:4]
        context["recruit_status"] = {
            "title": _("参加可能トーナメント"),
            "link": _("/tournament/register/"),
            "button": _("登録"),
            "display_register": True,
        }
        context["organizer_status"] = {
            "title": _("主催したトーナメント"),
            "link": _("/tournament/organized/"),
            "button": _("詳細"),
            "display_register": False,
        }
        context["participant_status"] = {
            "title": _("参加予定のトーナメント"),
            "link": _("/tournament/participant/"),
            "button": _("詳細"),
            "display_register": False,
        }

        return context

    def post(self, request):
        form = TournamentForm(self.request.POST)
        form.set_organizer(request.user)
        # form.set_only_user(self.request.POST.get("is_only_friend"))
        # tmp_res = super().form_valid(form)

        name = self.request.POST.get("name")
        start_at = self.request.POST.get("start_at")

        hour = self.request.POST.get("start_hour")
        minute = self.request.POST.get("start_minute")
        current_players = int(self.request.POST.get("current_players"))
        is_only_friend = (
            True if self.request.POST.get("is_only_friend") == "on" else False
        )
        organizer = request.user

        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", start_at) is None:
            return HttpResponseBadRequest()
        if re.fullmatch(r"\d{2}", hour) is None:
            return HttpResponseBadRequest()
        if re.fullmatch(r"\d{2}", minute) is None:
            return HttpResponseBadRequest()
        if current_players < 4 and current_players > 32:
            return HttpResponseBadRequest()
        if len(name) > 32:
            return HttpResponseBadRequest()
        print(f"{name=}")
        if re.search(r"[\'\"\;\*\#\=\%\<\>\/\(\)].", name):
            # if re.search(r"s", name):
            return HttpResponseBadRequest()

        Tournament.objects.create(
            name=name,
            organizer=organizer,
            start_at=start_at + "T" + hour + ":" + minute,
            is_only_friend=is_only_friend,
            current_players=current_players,
        )
        return HttpResponse()
