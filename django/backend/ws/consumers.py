import json
import jwt
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer

# from asgiref.sync import async_to_sync

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

    # ユーザーがオンラインになったとき
    async def info(self, event):
        print("info No.1")
        message = event["message"]
        print("info No.2")
        await self.send(text_data=message)
        print("info No.3")

    async def connect(self):
        try:
            session_id = self.scope["cookies"]["sessionid"]
            user = await get_user(session_id)

            if user.is_authenticated:
                group_name = self.room_group_name + str(user.id)
                print(f"connect No.5:{user.id=}")
                await self.channel_layer.group_add(group_name, self.channel_name)
                print("connect No.6")
                await self.channel_layer.group_send(
                    # await async_to_sync(self.channel_layer.group_send)(
                    group_name,  # グループ名
                    {
                        "type": "info",  # イベントタイプ
                        "message": "text_data",
                        # "user_id": user.id,
                        # "status": "online",  # 状態
                    },
                )
                print("connect No.7")
                await self.accept()  # WebSocket接続を受け入れる
                print("connect No.8")

            else:
                print("connect No.9")
                self.close()
            print("connect No.10")
        except Exception:
            print("Connect Exception Error")

    async def close(self, code=None, reason=None):
        print("close No.1")

    async def check(self, event):
        message = event["message"]
        await self.send(text_data=message)

    async def websocket_disconnect(self, message):
        print("websocket_disconnect No.1")
        session_id = self.scope["cookies"]["sessionid"]
        print("websocket_disconnect No.2")
        user = await get_user(session_id)
        print(f"websocket_disconnect No.3 {user.id=}")
        await update_user_login_state(user, False)

        group_name = self.room_group_name + str(user.id)
        print(f"websocket_disconnect No.4 {group_name=}")
        print("websocket_disconnect No.5")
        await self.channel_layer.group_send(
            group_name,
            {"type": "check", "message": "connection"},
        )
        print("websocket_disconnect No.6")

        print(message)
        pass

    async def disconnect(self, close_code):
        print("disconect No.1")
        try:
            print("disconect No.2")
            session_id = self.scope["cookies"]["sessionid"]
            user = await get_user(session_id)
            await update_user_login_state(user, False)
        except Exception:
            print("disconnect Exception Error")

    async def receive(self, text_data):
        print(f"receie No.0:{text_data=}")
        # from accounts.models import FtUser

        print(f"receie No.1:{text_data=}")

        session_id = self.scope["cookies"]["sessionid"]
        print(f"receie No.2:{text_data=}")
        user = await get_user(session_id)
        print(f"receie No.3:{text_data=}")
        if user.is_authenticated is False:
            return
        print(f"receie No.4:{text_data=}")

        # WebSocketでメッセージを受信したときに呼ばれる
        text_data_json = json.loads(text_data)
        print(f"receie No.2:{text_data_json=}")
        # message = text_data_json["message"]
        message_type = text_data_json["type"]
        print(f"receie No.3:{message_type=}")
        # print(f"No.1:{message_type=}")

        if message_type == "chat":
            print("receive Chat message")
        elif message_type == "connect":
            print("receive Connect message")

            group_name = self.room_group_name + str(user.id)
            await self.channel_layer.group_send(
                # await async_to_sync(self.channel_layer.group_send)(
                group_name,  # グループ名
                {
                    "type": "info",  # イベントタイプ
                    "message": "text_data",
                    # "user_id": user.id,
                    # "status": "online",  # 状態
                },
            )

            # content = text_data_json["content"]
            await update_user_login_state(user, True)

    async def send_personal_message(self, event):
        # Test

        # message = event["message"]

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
