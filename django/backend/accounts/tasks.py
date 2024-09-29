from celery import shared_task
from .models import FtTmpUser


@shared_task
def delete_tmp_user(user_id):
    user = FtTmpUser.objects.get(id=user_id)
    if user is not None:
        user.delete()


@shared_task
def change_login_state(user_id, flag):
    print("test change is_login No.1")
    user = FtTmpUser.objects.get(id=user_id)
    print("test change is_login No.2")
    if user is None:
        print("test change is_login No.3")
        return
    print("test change is_login No.4")
    user.is_login = flag
    print("test change is_login No.5")
    user.save()
    print("test change is_login No.6")
