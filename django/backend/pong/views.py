from django.shortcuts import render
from django.db import models
from django.db import IntegrityError, transaction

# from django.db.models import Q
from django.http import Http404
from django.views.decorators.http import condition
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from .models import MatchTmp
from django.db.models import Q

from tournament.models import Tournament, TournamentStatusChoices
from django.urls import reverse_lazy

from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    # HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)

import hashlib
import logging

from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# from django.utils.translation import gettext_lazy as _


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


class MatchView(DetailView):
    model = MatchTmp
    template_name = "pong/match.html"
    context_object_name = "match"


class TournamentDetail(TemplateView):
    def get(self, request):
        """
        GETは禁止
        """
        return HttpResponseNotFound()

    def post(self, request):
        try:
            tournament_id = 0
            data = {"id": tournament_id}

            tournaments = Tournament.objects.filter(
                start_at__lte=datetime.now(tz=timezone.utc),
                organizer=request.user,
                status=TournamentStatusChoices.ONGOING,
            ).order_by("start_at")
            if len(tournaments) == 0:
                return JsonResponse(data)

            tournament_id = tournaments[0].id
            data = {"id": tournament_id}
            return JsonResponse(data)
        except Exception as e:
            logger.error(f"StartPong Error:{e}")
            return HttpResponseBadRequest()


class StartPong(TemplateView):
    def get(self, request):
        """
        GETは禁止
        """
        return HttpResponseNotFound()

    def post(self, request):
        try:
            type = request.POST.get("type")
            id = 0
            tournament_id = None
            data = {"id": id}
            if type == "test":
                # 新しいmatchを作成したら、古いものは削除する
                tmp_match = MatchTmp.objects.filter(
                    player1=request.user, player2=None, tournament_id=None, round=None
                )
                for match in tmp_match:
                    match.delete()

                match = MatchTmp.objects.create(
                    player1=request.user,
                    player1_alias=request.user.username,
                    player2_alias="ANONYMOUS",
                )
                id = match.id
            elif type == "tournament":
                tournaments = Tournament.objects.filter(
                    start_at__lte=datetime.now(tz=timezone.utc),
                    organizer=request.user,
                    status=TournamentStatusChoices.ONGOING,
                ).order_by("start_at")
                print(f"tournament No.1:{len(tournaments)=}")
                if len(tournaments) == 0:
                    return JsonResponse(data)
                print(f"tournament No.2:{(tournaments[0].id)=}")
                list_matches = (
                    MatchTmp.objects.filter(tournament_id=tournaments[0], is_end=False)
                    .exclude(Q(player1=None) | Q(player2=None))
                    .order_by("-round")
                )
                print(f"tournament No.3:{len(list_matches)=}")

                if len(list_matches) == 0:
                    return JsonResponse(data)
                    # return JsonResponse(data)

                # for match in list_matches:
                # print(f"{match=},{match.player1=},")
                # print(f"{match=},{match.player2=},")
                id = list_matches[0].id
                tournament_id = tournaments[0].id
            else:
                logger.error("StartPong Error:not defined type")
                return HttpResponseBadRequest()
            data = {"id": id, "tournament": tournament_id}
            return JsonResponse(data)
        except Exception as e:
            logger.error(f"StartPong Error:{e}")
            return HttpResponseBadRequest()


def prepare_next_match(cur_match):
    try:

        if cur_match.player1_score >= 5:
            winer = cur_match.player1
            alias = cur_match.player1_alias
        else:
            winer = cur_match.player2
            alias = cur_match.player2_alias

        tournament = cur_match.tournament_id
        round = cur_match.round

        if round != 0:
            # try:
            # with transaction.atomic():
            list_matches = MatchTmp.objects.filter(
                tournament_id=tournament, is_end=False
            ).exclude(Q(player1=None) | Q(player2=None))
            if len(list_matches) > 0:
                return

            list = MatchTmp.objects.filter(
                tournament_id=tournament,
                is_end=True,
                is_other_game_end=False,
            )

            # list_matches.update(is_other_game_end=True)
            for match in list:

                if match.player2 is None:
                    winer = match.player1
                    alias = match.player1_alias
                elif match.player1_score >= 5:
                    winer = match.player1
                    alias = match.player1_alias
                else:
                    winer = match.player2
                    alias = match.player2_alias

                # tournament = match.tournament_id
                round = match.round
                next_round = int(round / 10)
                next_match = MatchTmp.objects.get(
                    tournament_id=tournament, round=next_round
                )
                if int(round % 2) == 1:
                    next_match.player1 = winer
                    next_match.player1_alias = alias
                else:
                    next_match.player2 = winer
                    next_match.player2_alias = alias
                next_match.save()
            list.update(is_other_game_end=True)
        else:
            tournament.status = TournamentStatusChoices.ENDED
            tournament.save()

    except Exception as e:
        logger.error(f"next Match Error:{e}")
    pass


class AddScore(UpdateView):
    model = MatchTmp
    fields = ["player1_score", "player2_score"]
    template_name = "user/profile.html"  # 使わない
    success_url = reverse_lazy("friend:friend")  # 使わない

    def get(self, request):
        """
        GETは禁止
        """
        return HttpResponseNotFound()

    def post(self, request, pk):
        try:
            player1_score = request.POST.get("player1_score")
            player2_score = request.POST.get("player2_score")
            match = MatchTmp.objects.get(id=pk)

            try:
                if match.is_end is False:
                    with transaction.atomic():
                        # 5点先取したら勝ち。それ以降は更新しない
                        if match.player1_score < 5 and match.player2_score < 5:
                            if player1_score == "1":
                                match.player1_score = match.player1_score + 1
                            elif player2_score == "1":
                                match.player2_score = match.player2_score + 1
                            match.save()
                        if match.player1_score >= 5 or match.player2_score >= 5:
                            match.is_end = True
                            match.save()
                            prepare_next_match(match)

                if match.player2 is None:
                    type = "test"
                else:
                    type = "tournament"
                score = {
                    "player1_score": match.player1_score,
                    "player2_score": match.player2_score,
                    "is_end": match.is_end,
                    "type": type,
                }
                return JsonResponse(score)
            except IntegrityError as e:
                logger.error(f"DB Error:{e}")
                return HttpResponseServerError()
        except Exception as e:
            logger.error(f"AddScore Error:{e}")
            return HttpResponseServerError()
