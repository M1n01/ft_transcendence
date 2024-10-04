from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView
from django.conf import settings
from django.db import IntegrityError, transaction

from .models import Tournament, TournamentParticipant, TournamentStatusChoices
from .forms import TournamentForm, TournamentParticipantForm

from django.http import (
    HttpResponseBadRequest,
    HttpResponse,
    JsonResponse,
)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import re
from datetime import datetime, timedelta, timezone
from pong.models import MatchTmp
from .tasks import create_matches


class RecruitingView(ListView):
    model = Tournament
    template_name = "tournament/list.html"
    context_object_name = "tournaments"
    paginate_by = 16

    def get_queryset(self):
        tmp_data = get_participants(self.request)
        return (
            Tournament.objects.exclude(id__in=tmp_data)
            .filter(status=TournamentStatusChoices.RECRUITING.value)
            .order_by("-start_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attr"] = {
            "title": _("参加可能トーナメント"),
            "link": "/tournament/recruiting/",
            "button": _("登録"),
            "display_register": True,
            "username": self.request.user.username,
        }

        return context


class OrganizedView(ListView):
    model = Tournament
    template_name = "tournament/list.html"
    context_object_name = "tournaments"
    paginate_by = 16

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
    paginate_by = 16

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


class AllView(ListView):
    model = Tournament
    template_name = "tournament/list.html"
    context_object_name = "tournaments"
    paginate_by = 16

    def get_queryset(self):
        return Tournament.objects.all().order_by("-start_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("すべてのトーナメント")
        return context


class RegisterApi(CreateView):
    model = TournamentParticipant
    form_class = TournamentParticipantForm
    template_name = "tournament/register.html"  # 使わない
    success_url = reverse_lazy("tournament:tournament")

    def get(self, request):
        return HttpResponse()

    def form_valid(self, form):
        try:
            data = self.request.POST.copy()
            data["participant"] = self.request.user
            data["participant_id"] = self.request.user.id
            data["is_accept"] = True
            form = TournamentParticipantForm(data)
            if form.is_valid():

                tournament = form.cleaned_data["tournament_id"]
                try:
                    with transaction.atomic():
                        participants = (
                            TournamentParticipant.objects.select_for_update().filter(
                                tournament_id=tournament
                            )
                        )
                        if len(participants) >= tournament.current_players:
                            data = {"is_full": True}
                            return JsonResponse(data, status=500)

                        # form.save() がうまくいかないので仕方なく
                        TournamentParticipant.objects.create(
                            tournament_id=tournament,
                            alias_name=form.cleaned_data["alias_name"],
                            participant=self.request.user,
                            is_accept=True,
                        )
                except IntegrityError:
                    data = {"is_full": False}
                    return JsonResponse(data, status=500)

                participants = TournamentParticipant.objects.select_for_update().filter(
                    tournament_id=tournament
                )
                if len(participants) == tournament.current_players:
                    create_matches(tournament)
                    tournament.status = TournamentStatusChoices.ONGOING
                    tournament.save()
        except Exception as e:
            print(f"{e=}")
            data = {"is_full": False}
            return JsonResponse(data, status=500)
        return HttpResponse()


def get_participants(request):
    tmp_participant = TournamentParticipant.objects.filter(
        participant=request.user, is_accept=True
    )
    return tmp_participant.values_list("tournament_id", flat=True)


class TournamentView(LoginRequiredMixin, CreateView):
    form_class = TournamentForm
    template_name = "tournament/tournament.html"

    def get_recruiting_data(self):
        tmp_data = get_participants(self.request)
        return (
            Tournament.objects.exclude(id__in=tmp_data)
            .filter(status=TournamentStatusChoices.RECRUITING.value)
            .order_by("-start_at")
        )[:4]

    def get_participant_data(self):
        tmp_data = get_participants(self.request)
        return Tournament.objects.filter(id__in=tmp_data).order_by("-start_at")[:4]

    def get_organizer_data(self):
        return Tournament.objects.filter(organizer=self.request.user).order_by(
            "-start_at"
        )[:4]

    def get_old_data(self):
        return Tournament.objects.filter(status=TournamentStatusChoices.ENDED).order_by(
            "-start_at"
        )[:4]

    def get_all_data(self):
        return Tournament.objects.all().order_by("-start_at")[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recruiting"] = self.get_recruiting_data()
        context["as_participant"] = self.get_participant_data()
        context["as_organizer"] = self.get_organizer_data()
        context["old"] = self.get_old_data()
        context["all"] = self.get_all_data()

        context["recruit_status"] = {
            "title": _("参加可能トーナメント"),
            "link": "/tournament/recruiting/",
            "button": _("登録"),
            "display_register": True,
            "username": self.request.user.username,
        }
        context["organizer_status"] = {
            "title": _("主催したトーナメント"),
            "link": "/tournament/organized/",
            "button": _("詳細"),
            "display_register": False,
        }
        context["participant_status"] = {
            "title": _("参加予定のトーナメント"),
            "link": "/tournament/participant/",
            "button": _("詳細"),
            "display_register": False,
        }
        context["old_status"] = {
            "title": _("終了したトーナメント"),
            "link": "/tournament/old/",
            "button": _("詳細"),
            "display_register": False,
        }
        context["all_status"] = {
            "title": _("すべてのーナメント"),
            "link": "/tournament/all/",
            "button": _("詳細"),
            "display_register": False,
        }

        return context

    def post(self, request):
        form = TournamentForm(self.request.POST)
        form.set_organizer(request.user)

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
        if re.search(r"[\'\"\;\*\#\=\%\<\>\/\(\)].", name):
            return HttpResponseBadRequest()

        now = datetime.now(tz=timezone.utc) + timedelta(minutes=10)
        fmt = "%Y-%m-%d %H:%M"
        fmt2 = "%Y-%m-%dT%H:%M"
        datetime_str = start_at + " " + hour + ":" + minute
        hour = getattr(settings, "TIME_HOURS", None)

        dt = datetime.strptime(datetime_str, fmt) - timedelta(hours=hour)
        dt = dt.replace(tzinfo=timezone.utc)
        dt.replace(second=0)
        if now > dt:
            return HttpResponseBadRequest()

        dt_str = datetime.strftime(dt, fmt2)

        Tournament.objects.create(
            name=name,
            organizer=organizer,
            start_at=dt_str,
            is_only_friend=is_only_friend,
            current_players=current_players,
        )
        return HttpResponse()


def updateTournamentStatus(pk, status, number=0):
    tournament = Tournament.objects.get(pk=pk)
    tournament["status"] = status
    if number != 0:
        tournament["current_players"] = number
    tournament.save()


class DetailView(DetailView):
    model = Tournament
    template_name = "tournament/detail.html"
    context_object_name = "tournament"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = context[self.context_object_name].id
        participants = TournamentParticipant.objects.filter(tournament_id=id)
        context["len_participants"] = len(participants)
        if len(participants) > 0:
            context["participants"] = participants
        else:
            context["participants"] = _("参加者はいません")

        return context


class InfoApi(DetailView):
    model = Tournament
    template_name = "tournament/detail.html"
    context_object_name = "tournament"

    def get(self, request, pk, **kwargs):
        tournament = Tournament.objects.get(pk=pk)
        participants = TournamentParticipant.objects.filter(tournament_id=tournament)
        matches = MatchTmp.objects.filter(tournament_id=tournament)
        match_data = [
            {
                "id": match.round,
                "player1": match.player1.username if match.player1 is not None else "",
                "player2": match.player2.username if match.player2 is not None else "",
                "player1_score": match.player1_score,
                "player2_score": match.player2_score,
            }
            for match in matches
        ]
        data = {
            "max_user_cnt": len(participants),
            "name": tournament.name,
            "matches": match_data,
        }
        return JsonResponse(data)
