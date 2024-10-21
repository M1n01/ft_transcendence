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


def create_first_match(seed_array, tournament, participants, player_id, round, id):
    if id in seed_array:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round * 10 + 1,
            player1=participants[player_id].participant,
            player1_alias=participants[player_id].alias_name,
            is_end=True,
        )

        next_match = MatchTmp.objects.get(tournament_id=tournament, round=round)
        if round % 2 == 1:
            next_match.player1 = participants[player_id].participant
            next_match.player1_alias = participants[player_id].alias_name
        else:
            next_match.player2 = participants[player_id].participant
            next_match.player2_alias = participants[player_id].alias_name
        next_match.save()
        player_id = player_id + 1

    else:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round * 10 + 1,
            player1=participants[player_id].participant,
            player2=participants[player_id + 1].participant,
            player1_alias=participants[player_id].alias_name,
            player2_alias=participants[player_id + 1].alias_name,
        )
        player_id = player_id + 2

    if id + 1 in seed_array:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round * 10 + 2,
            player1=participants[player_id].participant,
            player1_alias=participants[player_id].alias_name,
            is_end=True,
        )

        next_match = MatchTmp.objects.get(tournament_id=tournament, round=round)
        if round % 2 == 1:
            next_match.player1 = participants[player_id].participant
            next_match.player1_alias = participants[player_id].alias_name
        else:
            next_match.player2 = participants[player_id].participant
            next_match.player2_alias = participants[player_id].alias_name
        next_match.save()
        player_id = player_id + 1

    else:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round * 10 + 2,
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
    tmp_players_size = players_size
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
    MatchTmp.objects.create(tournament_id=tournament, round=1)
    MatchTmp.objects.create(tournament_id=tournament, round=2)
    depth = depth - 1

    round_array = [1, 2]
    player_id = 0
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
    print("my_task No.1")
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
    print("my_task No.2")
    print(f"{result=}")
    print("my_task No.3")
    print(f"{now=}")
    return result


@shared_task
@transaction.atomic
def close_application():
    """
    トーナメントの応募締切タイミグで実行される
    参加者の人数が4人未満なら中止となり、4人以上ならトーナメントが開始される

    """
    logger.info("close tournament")

    path = "/workspace/uesr4.txt"
    f = open(path, "w")
    now = datetime.now()
    f.write("abcdefg")  # 何も書き込まなくてファイルは作成されました
    f.write(f"now:{now=}")  # 何も書き込まなくてファイルは作成されました
    f.close()

    try:
        start = datetime.now(timezone.utc)
        end = start + timedelta(minutes=10)
        list = Tournament.objects.filter(
            # start_at__gte=start,
            start_at__lte=end,
            status=TournamentStatusChoices.RECRUITING,
        )

        path = "/workspace/uesr5.txt"
        f = open(path, "w")
        now = datetime.now()
        f.write("abcdefg")  # 何も書き込まなくてファイルは作成されました
        f.write(f"now:{now=}")  # 何も書き込まなくてファイルは作成されました
        f.write(f"now:{len(list)=}")  # 何も書き込まなくてファイルは作成されました
        f.close()

        for tournament in list:
            path = "/workspace/uesr6.txt"
            f = open(path, "w")
            now = datetime.now()
            f.write("abcdefg")  # 何も書き込まなくてファイルは作成されました
            f.close()

            participant = TournamentParticipant.objects.filter(
                tournament_id=tournament.id
            )
            path = "/workspace/uesr7.txt"
            f = open(path, "w")
            now = datetime.now()
            f.write("abcdefg")  # 何も書き込まなくてファイルは作成されました
            f.write(f"now:{now=}")  # 何も書き込まなくてファイルは作成されました
            f.write(f"now:{len(list)=}")  # 何も書き込まなくてファイルは作成されました
            f.close()

            if len(participant) < tournament.current_players:
                tournament.status = TournamentStatusChoices.CANCEL
            else:
                create_matches(tournament)
                tournament.status = TournamentStatusChoices.ONGOING

            path = "/workspace/uesr10.txt"
            f = open(path, "w")
            now = datetime.now()
            f.write("abcdefg")  # 何も書き込まなくてファイルは作成されました
            f.write(f"now:{now=}")  # 何も書き込まなくてファイルは作成されました
            f.close()

            tournament.save()

        path = "/workspace/uesr11.txt"
        f = open(path, "w")
        now = datetime.now()
        f.write("abcdefg")  # 何も書き込まなくてファイルは作成されました
        f.write(f"now:{now=}")  # 何も書き込まなくてファイルは作成されました
        f.close()
    except Exception as e:
        logger.error(f"Error close_application():{e}")
