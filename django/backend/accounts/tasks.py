from celery import shared_task
from .models import FtTmpUser


@shared_task
def delete_tmp_user(user_id):
    user = FtTmpUser.objects.get(id=user_id)
    if user is not None:
        user.delete()
