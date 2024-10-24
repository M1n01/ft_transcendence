from celery import shared_task
from .models import FtTmpUser

import logging

logger = logging.getLogger(__name__)


@shared_task
def delete_tmp_user(user_id):
    try:
        users = FtTmpUser.objects.filter(id=user_id)
        if len(users) == 0:
            return
        users[0].delete()
    except Exception as e:
        logger.error(f"Delete Tmp User Error:{e}")


@shared_task
def change_login_state(user_id, flag):
    users = FtTmpUser.objects.filter(id=user_id)
    if len(users) == 0:
        return
    user = users[0]
    user.is_login = flag
    user.save()


@shared_task
def check_login_state(user_id, flag):
    users = FtTmpUser.objects.filter(id=user_id)
    if len(users) == 0:
        return
    user = users[0]
    if user is None:
        return
