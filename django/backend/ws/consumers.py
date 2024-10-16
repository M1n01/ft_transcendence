import json
import jwt
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer

# from accounts.models import FtUser
from .message import get

# from .message import get, post

from channels.db import database_sync_to_async


@database_sync_to_async
def update_user_login_state(user, flag):
    user.is_login = flag
    user.save()


def decode(session_id):
    try:
        return jwt.decode(
            session_id,
            getattr(settings, "SECRET_KEY", None),
            leeway=5,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError as e:
        print(f"Ignore:{e=}")
        # そのまま例外で処理を終わらせる
        raise Exception
    except jwt.exceptions.DecodeError as e:
        print(f"Ignore:{e=}")
        raise Exception


@database_sync_to_async
def get_user(session_id):
    from accounts.models import FtUser

    json = decode(session_id)
    id = json["sub"]
    return FtUser.objects.get(id=id)


class FtWebsocket(AsyncWebsocketConsumer):
    room_group_name = "ws-"
    tmp_group_name = "test_group"

    # ユーザーがオンラインになったとき
    async def info(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps({"type": "info", "method": "post", "message": message})
        )

    async def get(self, event):
        """
        クライアント側にデータを要求する
        """
        message = event["message"]
        param1 = event["param1"]
        param2 = event["param2"]
        param3 = event["param3"]
        param4 = event["param4"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "get",
                    "message": message,
                    "param1": param1,
                    "param2": param2,
                    "param3": param3,
                    "param4": param4,
                }
            )
        )

    async def post(self, event):
        """
        クライアント側にデータを送るだけ
        """
        message = event["message"]
        param1 = event["param1"]
        param2 = event["param2"]
        param3 = event["param3"]
        param4 = event["param4"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "post",
                    "message": message,
                    "param1": param1,
                    "param2": param2,
                    "param3": param3,
                    "param4": param4,
                }
            )
        )

    async def connect(self):
        try:
            session_id = self.scope["cookies"]["sessionid"]
            user = await get_user(session_id)

            if user.is_authenticated:
                group_name = self.room_group_name + str(user.username)
                await self.channel_layer.group_add(group_name, self.channel_name)
                await self.accept()  # WebSocket接続を受け入れる
                await update_user_login_state(user, True)

            else:
                self.close()
        except Exception:
            print("Connect Exception Error")

    async def close(self, code=None, reason=None):
        print("close")

    async def check(self, event):
        message = event["message"]
        await self.send(text_data=message)

    async def websocket_disconnect(self, message):
        session_id = self.scope["cookies"]["sessionid"]
        user = await get_user(session_id)
        await update_user_login_state(user, False)

        group_name = self.room_group_name + str(user.username)
        await self.channel_layer.group_send(
            group_name,
            {
                "type": "get",
                "message": "Let me know your alive",
                "param1": "",
                "param2": "",
                "param3": "",
                "param4": "",
            },
        )

    async def handle_post_method(self, user, json):
        if json["message"] == "active":
            await update_user_login_state(user, True)

    async def handle_get_method(self, user, json):
        message = ""
        if json["message"] == "active_list":
            (message, param1, param2, param3, param4) = await get.active(json)

        group_name = self.room_group_name + str(user.username)
        if message == "":
            return
        await self.channel_layer.group_send(
            group_name,
            {
                "type": "post",
                "message": message,
                "param1": param1,
                "param2": param2,
                "param3": param3,
                "param4": param4,
            },
        )

    async def receive(self, text_data):
        session_id = self.scope["cookies"]["sessionid"]
        user = await get_user(session_id)
        if user.is_authenticated is False:
            return

        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json["type"]
            if message_type == "get":
                await self.handle_get_method(user, text_data_json)
            elif message_type == "post":
                await self.handle_post_method(user, text_data_json)
        except Exception as e:
            print(f"Websocket Error:{e}")

    async def send_personal_message(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "status": "online",
                    "user_id": "user_id",
                }
            )
        )

    async def is_online(self, event):
        message = event["message"]
        await self.send(text_data=message)
