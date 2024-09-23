# from django.backend.ft_trans.celery import shared_task  # type: ignore
from celery import shared_task


@shared_task()
def hello_world():
    print("start hello_world")
    print("hello")
    print("-----" * 200)
    print("end hello_world")


@shared_task()
def calc(a: int, b: int) -> int:
    result: int = a + b
    return result


@shared_task
def my_task(arg1, arg2):
    print("my_task No.1")
    path = "/workspace/uesr2.txt"
    f = open(path, "w")
    f.write("abcdefg")  # 何も書き込まなくてファイルは作成されました
    f.close()
    # Task logic here
    result = arg1 + arg2
    print("my_task No.2")
    print(f"{result=}")
    print("my_task No.3")
    return result
