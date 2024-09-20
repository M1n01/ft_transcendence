# from django.shortcuts import render
# from django.db import models
# from django.http import Http404
# from django.views.decorators.http import condition
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView

from .models import Tournament, TournamentParticipant, TournamentStatusChoices
from .forms import TournamentForm, TournamentParticipantForm

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
    paginate_by = 3

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


class RegisterApi(CreateView):
    model = TournamentParticipant
    form_class = TournamentParticipantForm
    template_name = "tournament/register.html"  # 使わない
    success_url = reverse_lazy("tournament:tournament")

    def get(self, request):
        return HttpResponse()

    def form_valid(self, form):
        # モデルを保存する
        try:
            data = self.request.POST.copy()
            data["participant"] = self.request.user
            data["participant_id"] = self.request.user.id
            data["is_accept"] = True
            form = TournamentParticipantForm(data)
            if form.is_valid():
                # form.save() がうまくいかないので仕方なく

                TournamentParticipant.objects.create(
                    tournament_id=form.cleaned_data["tournament_id"],
                    alias_name=form.cleaned_data["alias_name"],
                    participant=self.request.user,
                    is_accept=True,
                )
        except Exception as e:
            print(f"{e=}")
            return HttpResponseServerError()
        return HttpResponse()

    # def form_invalid(self, form):
    # return HttpResponseBadRequest()

    pass


# class TournamentView(TemplateView):
class TournamentView(LoginRequiredMixin, CreateView):
    # model = Tournament
    # form = TournamentForm
    form_class = TournamentForm
    template_name = "tournament/tournament.html"

    def get_participants(self):
        tmp_participant = TournamentParticipant.objects.filter(
            participant=self.request.user, is_accept=True
        )
        return tmp_participant.values_list("tournament_id", flat=True)

    def get_recruiting_data(self):
        tmp_data = self.get_participants()
        return (
            Tournament.objects.exclude(id__in=tmp_data)
            .filter(status=TournamentStatusChoices.RECRUITING.value)
            .order_by("-start_at")
        )[:4]

    def get_participant_data(self):
        tmp_data = self.get_participants()
        return Tournament.objects.filter(id__in=tmp_data).order_by("-start_at")[:4]

    def get_organizer_data(self):
        return Tournament.objects.filter(organizer=self.request.user).order_by(
            "-start_at"
        )[:4]

    def get_old_data(self):
        return Tournament.objects.filter(status=TournamentStatusChoices.ENDED).order_by(
            "-start_at"
        )[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recruiting"] = self.get_recruiting_data()
        context["as_participant"] = self.get_participant_data()
        context["as_organizer"] = self.get_organizer_data()
        context["old"] = self.get_old_data()

        context["recruit_status"] = {
            "title": _("参加可能トーナメント"),
            "link": _("/tournament/register/"),
            "button": _("登録"),
            "display_register": True,
            "username": self.request.user.username,
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
        context["old_status"] = {
            "title": _("終了したトーナメント"),
            "link": _("/tournament/old/"),
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
