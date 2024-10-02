from channels.db import database_sync_to_async


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
    print("get_active No.1")
    list = json["content"].split("-")
    print("get_active No.2")
    if len(list) == 0:
        return ("", "", "", "", "")
    print("get_active No.3")
    param1 = await get_users_active(list)
    print("get_active No.4")
    message = "active_list"
    return (message, param1, "", "", "")
