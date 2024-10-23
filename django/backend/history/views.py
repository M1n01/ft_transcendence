from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import FtUser
from tournament.models import Tournament
from django.db.models import Q
from django.core.paginator import Paginator

from pong.models import MatchTmp
import datetime

import logging

logger = logging.getLogger(__name__)

# Create your views here.


def edit_matches_data(request, matches):
    try:
        for data in matches:
            data["draw"] = False
            data["win"] = False
            data["lose"] = False
            data["invalid"] = False
            data["opponent"] = "Test"
            if data["player1_score"] > data["player2_score"]:
                winer = data["player1_id"]
            elif data["player1_score"] < data["player2_score"]:
                winer = data["player2_id"]
            else:
                if data["player1_score"] == 0:
                    data["invalid"] = True
                else:
                    data["draw"] = True
            if winer == request.user.id:
                data["win"] = True
            else:
                data["lose"] = True

            if data["player1_id"] == request.user.id:
                data["opponent"] = FtUser.objects.get(id=data["player2_id"])
                data["opponent_name"] = FtUser.objects.get(
                    id=data["player2_id"]
                ).username
                data["result"] = f"{data['player1_score']} - {data['player2_score']}"
            else:
                data["opponent"] = FtUser.objects.get(id=data["player1_id"])
                data["opponent_name"] = FtUser.objects.get(
                    id=data["player1_id"]
                ).username
                data["result"] = f"{data['player2_score']} - {data['player1_score']}"
    except Exception as e:
        logger.error(f"edit_matches_data error:{e=}")
        matches = []

    paginator = Paginator(matches, 16)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return (matches, page_obj)


def get_tournament(request):
    list = FtUser.objects.all()
    list2 = Tournament.objects.all()
    matches = [
        {
            "tournament_id": list2[0].id,
            "round": 12,
            "player1_id": list[0].id,
            "player2_id": list[1].id,
            "player1_score": 2,
            "player2_score": 5,
            "updated_at": datetime.datetime.now(),
        },
        {
            "tournament_id": list2[1].id,
            "round": 121,
            "player1_id": list[2].id,
            "player2_id": list[3].id,
            "player1_score": 3,
            "player2_score": 2,
            "updated_at": datetime.datetime.now(),
        },
        {
            "tournament_id": list2[0].id,
            "round": 1,
            "player1_id": list[4].id,
            "player2_id": list[5].id,
            "player1_score": 1,
            "player2_score": 0,
            "updated_at": datetime.datetime.now(),
        },
        {
            "tournament_id": list2[1].id,
            "round": 0,
            "player1_id": list[6].id,
            "player2_id": list[7].id,
            "player1_score": 2,
            "player2_score": 4,
            "updated_at": datetime.datetime.now(),
        },
        {
            "tournament_id": list2[0].id,
            "round": 2121,
            "player1_id": list[8].id,
            "player2_id": None,
            "player1_score": 0,
            "player2_score": 0,
            "updated_at": datetime.datetime.now(),
        },
    ]

    # matches = MatchTmp.objects.filter("")
    # matches = MatchTmp.objects.filter(
    #    Q(player1=request.user) | Q(player2=request.user)
    # ).order_by("-updated_at")

    list = []
    for match in matches:
        if (match["player1_id"] is not None) and (match["player2_id"] is not None):
            # シード選は除く
            list.append(match)

    (list, page_obj) = edit_matches_data(request, list)
    return (list, page_obj)


def get_ovo(request):
    matches = MatchTmp.objects.filter(
        Q(player1=request.user) | Q(player2=request.user)
    ).order_by("-updated_at")

    # トーナメントと合わせるために配列に変換する
    list = []
    for match in matches:
        list.append(
            {
                "tournament_id": match.tournament_id,
                "round": match.round,
                "player1_id": match.player1_id,
                "player2_id": match.player2_id,
                "player1_score": match.player1_id,
                "player2_score": match.player2_id,
                "updated_at": match.updated_at,
            }
        )

    (list, page_obj) = edit_matches_data(request, list)
    return (list, page_obj)


class History(TemplateView):
    # template_name = "history/history.html"

    def get(self, request):
        (tournaments, _) = get_tournament(self.request)
        (ovo, _) = get_ovo(self.request)[:4]
        context = {"one_v_one": ovo, "tournaments": tournaments[:4]}

        return render(request, "history/history.html", context)


class TournamentMatch(TemplateView):
    def get(self, request):
        (tournaments, page_obj) = get_tournament(self.request)
        context = {"tournaments": tournaments, "page_obj": page_obj}

        return render(request, "history/tournaments-list.html", context)


class OVOMatch(TemplateView):
    def get(self, request):
        (ovo, page_obj) = get_ovo(self.request)[:4]
        context = {"ovos": ovo, "page_obj": page_obj}

        return render(request, "history/ovo-list.html", context)
