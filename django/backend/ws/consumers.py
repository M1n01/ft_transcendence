import json
import jwt
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer

# from channels.generic.websocket import JsonWebsocketConsumer
# from channels.auth import login
from channels.db import database_sync_to_async


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
    print(f"{id=}")
    return FtUser.objects.get(id=id)
    # return ""


class FtWebsocket(AsyncWebsocketConsumer):
    room_group_name = "websocket"

    async def connect(self):

        session_id = self.scope["cookies"]["sessionid"]
        user = await get_user(session_id)

        # self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # await self.accept()  # WebSocket接続を受け入れる
        if user.is_authenticated:
            print("accept No.1")
            self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()  # WebSocket接続を受け入れる
            # user.is_login = True
            print("accept No.2")
            # await user.save()
            print("accept No.3")
        else:
            self.close()

    async def disconnect(self, close_code):
        print("Websocket Disconnect")
        # user.is_login = False
        # user.save()
        # WebSocket切断時に呼ばれる
        pass

    async def receive(self, text_data):
        # print(f"ws user:{self.user.username}")
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
        message = event["message"]

        # WebSocketにメッセージを送信
        await self.send(text_data=message)
