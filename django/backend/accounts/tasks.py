from celery import shared_task
from .models import FtTmpUser


@shared_task
def delete_tmp_user(user_id):
    user = FtTmpUser.objects.get(id=user_id)
    if user is not None:
        user.delete()


@shared_task
def change_login_state(user_id, flag):
    user = FtTmpUser.objects.get(id=user_id)
    if user is None:
        return
    user.is_login = flag
    user.save()


@shared_task
def check_login_state(user_id, flag):
    print("check_login_state No.1")
    user = FtTmpUser.objects.get(id=user_id)
    if user is None:
        return
    # user.is_login = flag
    # user.save()
