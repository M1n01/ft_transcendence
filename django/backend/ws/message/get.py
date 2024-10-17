from channels.db import database_sync_to_async
from django.db.models import Q


async def send_is_alive(self, event):
    await self.channel_layer.group_send(
        self.user_group_name,
        {
            "type": "is_alive",
            "message": "is_alive",
        },
    )
    message = event["message"]
    await self.send(text_data=message)


async def is_alive(self, event):
    message = event["message"]
    await self.send(text_data=message)


@database_sync_to_async
def get_users_active(list):
    from accounts.models import FtUser

    users = FtUser.objects.filter(id__in=list)
    if len(users) == 0:
        return ""

    users_active = "{"
    for user in users:
        users_active = users_active + f'"{user.id}":"{str(user.is_login)}",'
    users_active = users_active[0:-1]
    users_active = users_active + "}"
    return users_active


async def active(json):
    list = json["content"].split("@")
    if len(list) == 0:
        return ("", "", "", "", "")
    param1 = await get_users_active(list)
    message = "active_list"
    return (message, param1, "", "", "")


@database_sync_to_async
def get_alert_cnt(user):
    from notification.models import UserNotification

    list = UserNotification.objects.filter(Q(user=user) & Q(is_read=False))
    return len(list)


async def alert_cnt(user):
    param1 = await get_alert_cnt(user)
    message = "alert_cnt"
    return (message, param1, "", "", "")
