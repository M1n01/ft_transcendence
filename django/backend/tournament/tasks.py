# from django.backend.ft_trans.celery import shared_task  # type: ignore

# from ft_trans.celery import app
from celery import shared_task
from datetime import datetime, timezone, timedelta
from .models import TournamentStatusChoices, Tournament, TournamentParticipant
from pong.models import MatchTmp
import random


def create_first_match(seed_array, tournament, participants, player_id, round, id):
    if id in seed_array:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round * 10 + 1,
            player1=participants[player_id].participant,
        )
        player_id = player_id + 1
    else:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round * 10 + 1,
            player1=participants[player_id].participant,
            player2=participants[player_id + 1].participant,
        )
        player_id = player_id + 2

    if id + 1 in seed_array:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round * 10 + 2,
            player1=participants[player_id].participant,
        )
        player_id = player_id + 1
    else:
        MatchTmp.objects.create(
            tournament_id=tournament,
            round=round * 10 + 2,
            player1=participants[player_id].participant,
            player2=participants[player_id + 1].participant,
        )
        player_id = player_id + 2
    return player_id


def create_matches(tournament):
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
        print(f"{i=}")
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
def close_application():
    start = datetime.now(timezone.utc)
    end = start + timedelta(minutes=15)
    list = Tournament.objects.filter(start_at__gte=start, start_at__lte=end)
    for tournament in list:
        participant = TournamentParticipant.objects.filter(tournament_id=tournament.id)
        if len(participant) < 4:
            tournament.status = TournamentStatusChoices.CANCEL
        else:
            create_matches(tournament)
            tournament.status = TournamentStatusChoices.ONGOING
        tournament.save()
