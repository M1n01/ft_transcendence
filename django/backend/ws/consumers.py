import json
import jwt
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer

# from accounts.tasks import change_login_state

# from channels.generic.websocket import JsonWebsocketConsumer
# from channels.auth import login
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

    async def connect(self):
        try:
            session_id = self.scope["cookies"]["sessionid"]
            user = await get_user(session_id)

            if user.is_authenticated:
                group_name = self.room_group_name + user.id
                self.channel_layer.group_add(group_name, self.channel_name)
                await self.accept()  # WebSocket接続を受け入れる
                await update_user_login_state(user, True)
            else:
                self.close()
        except Exception:
            print("Connect Exception Error")

    async def disconnect(self, close_code):
        try:
            session_id = self.scope["cookies"]["sessionid"]
            user = await get_user(session_id)
            await update_user_login_state(user, False)
        except Exception:
            print("disconnect Exception Error")

    async def receive(self, text_data):
        # Test

        # WebSocketでメッセージを受信したときに呼ばれる
        text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        message_type = text_data_json["type"]
        # print(f"No.1:{message_type=}")

        if message_type == "chat":
            print(f"No.2:{message_type=}")
        elif message_type == "connect":
            print(f"No.3:{message_type=}")
        await self.send(
            text_data=json.dumps(
                {"type": "notification", "content": "Notification processed."}
            )
        )

    async def send_personal_message(self, event):
        # Test

        message = event["message"]

        # WebSocketにメッセージを送信
        await self.send(text_data=message)

    async def send(self, type, message):
        session_id = self.scope["cookies"]["sessionid"]
        user = await get_user(session_id)

        if user.is_authenticated:
            await self.channel_layer.group_send(
                self.user_group_name,
                {
                    "type": type,
                    "message": message,
                },
            )

    async def is_online(self, event):
        message = event["message"]
        await self.send(text_data=message)
