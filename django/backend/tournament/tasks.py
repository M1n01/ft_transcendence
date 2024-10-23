# from django.backend.ft_trans.celery import shared_task  # type: ignore

# from ft_trans.celery import app
from celery import shared_task
from datetime import datetime, timezone, timedelta
from .models import TournamentStatusChoices, Tournament, TournamentParticipant
from pong.models import MatchTmp
from django.db import transaction
import random
import logging

logger = logging.getLogger(__name__)


def create_first_match(seed_array, tournament, participants, player_id, round_id, id):
    if round_id == 0:
        return
    if id in seed_array:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round_id * 10 + 1,
            player1=participants[player_id].participant,
            player1_alias=participants[player_id].alias_name,
            is_end=True,
        )

        next_match = MatchTmp.objects.get(tournament_id=tournament, round=round_id)
        # if round_id % 2 == 1:
        next_match.player1 = participants[player_id].participant
        next_match.player1_alias = participants[player_id].alias_name
        # else:
        # next_match.player2 = participants[player_id].participant
        # next_match.player2_alias = participants[player_id].alias_name
        next_match.save()
        player_id = player_id + 1
        # return

    else:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round_id * 10 + 1,
            player1=participants[player_id].participant,
            player2=participants[player_id + 1].participant,
            player1_alias=participants[player_id].alias_name,
            player2_alias=participants[player_id + 1].alias_name,
        )
        player_id = player_id + 2

    # round_id = seed_array[id + 1]
    if id + 1 in seed_array:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round_id * 10 + 2,
            player1=participants[player_id].participant,
            player1_alias=participants[player_id].alias_name,
            is_end=True,
        )

        next_match = MatchTmp.objects.get(tournament_id=tournament, round=round_id)
        # if round_id % 2 == 0:
        # next_match.player1 = participants[player_id].participant
        # next_match.player1_alias = participants[player_id].alias_name
        # else:
        next_match.player2 = participants[player_id].participant
        next_match.player2_alias = participants[player_id].alias_name
        next_match.save()
        player_id = player_id + 1

    else:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round_id * 10 + 2,
            player1=participants[player_id].participant,
            player2=participants[player_id + 1].participant,
            player1_alias=participants[player_id].alias_name,
            player2_alias=participants[player_id + 1].alias_name,
        )
        player_id = player_id + 2
    return player_id


def create_matches(tournament):
    """
    トーナメント表を描画するために、pongゲーム用のMatchを作成する
    """
    if tournament.status != TournamentStatusChoices.RECRUITING:
        return

    participants = TournamentParticipant.objects.filter(tournament_id=tournament)
    players_size = len(participants)
    tmp_players_size = players_size - 1
    depth = -1
    while tmp_players_size >= 1:
        tmp_players_size = int(tmp_players_size / 2)
        depth = depth + 1
    first_match_size = 2**depth
    seed_match_size = 2 * first_match_size - players_size
    seed_array = []
    while len(seed_array) <= seed_match_size - 1:
        i = random.randint(0, first_match_size - 1)
        if i not in seed_array:
            seed_array.append(i)

    MatchTmp.objects.create(tournament_id=tournament, round=0)
    if players_size == 4:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=1,
            player1=participants[0].participant,
            player1_alias=participants[0].alias_name,
            player2=participants[1].participant,
            player2_alias=participants[1].alias_name,
        )
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=2,
            player1=participants[2].participant,
            player1_alias=participants[2].alias_name,
            player2=participants[3].participant,
            player2_alias=participants[3].alias_name,
        )
    else:
        MatchTmp.objects.create(tournament_id=tournament, round=1)
        MatchTmp.objects.create(tournament_id=tournament, round=2)

    depth = depth - 1
    player_id = 0

    round_array = [1, 2]
    while depth != 0:
        tmp_round_array = []
        id = 0
        for round in round_array:
            tmp_round_array.append(round * 10 + 1)
            tmp_round_array.append(round * 10 + 2)
            if depth == 1:
                player_id = create_first_match(
                    seed_array, tournament, participants, player_id, round, id
                )
            else:
                MatchTmp.objects.create(tournament_id=tournament, round=round * 10 + 1)
                MatchTmp.objects.create(tournament_id=tournament, round=round * 10 + 2)
            id = id + 2
        round_array = tmp_round_array
        depth = depth - 1


@shared_task
def my_task(arg1, arg2):
    path = "/workspace/uesr2.txt"
    f = open(path, "w")
    now = datetime.now()
    f.write("abcdefg")  # 何も書き込まなくてファイルは作成されました
    f.write(f"now:{now=}")  # 何も書き込まなくてファイルは作成されました
    f.write(f"{arg1=}")  # 何も書き込まなくてファイルは作成されました
    f.write(f"{arg2=}")  # 何も書き込まなくてファイルは作成されました
    f.close()
    # Task logic here
    result = arg1 + arg2
    return result


@shared_task
@transaction.atomic
def close_application():
    """
    トーナメントの応募締切タイミグで実行される
    参加者の人数が4人未満なら中止となり、4人以上ならトーナメントが開始される

    """
    logger.info("close tournament")

    try:
        start = datetime.now(timezone.utc)
        end = start + timedelta(minutes=10)
        list = Tournament.objects.filter(
            # start_at__gte=start,
            start_at__lte=end,
            status=TournamentStatusChoices.RECRUITING,
        )

        for tournament in list:

            participant = TournamentParticipant.objects.filter(
                tournament_id=tournament.id
            )

            if len(participant) < 4:
                tournament.status = TournamentStatusChoices.CANCEL
            else:
                create_matches(tournament)
                tournament.status = TournamentStatusChoices.ONGOING

            tournament.save()

    except Exception as e:
        logger.error(f"Error close_application():{e}")
