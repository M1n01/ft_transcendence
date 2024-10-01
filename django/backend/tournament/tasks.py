# from django.backend.ft_trans.celery import shared_task  # type: ignore

# from ft_trans.celery import app
from celery import shared_task
from datetime import datetime, timezone, timedelta
from .models import TournamentStatusChoices, Tournament, TournamentParticipant


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
            tournament.status = TournamentStatusChoices.ONGOING
        tournament.save()
