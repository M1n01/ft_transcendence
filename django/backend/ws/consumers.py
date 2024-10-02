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
    print("update_user_login_state No.1")
    user.is_login = flag
    print("update_user_login_state No.2")
    user.save()
    print("update_user_login_state No.3")


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
        print("info No.1")
        message = event["message"]
        print("info No.2")
        # await self.send(text_data=message)
        await self.send(
            text_data=json.dumps({"type": "info", "method": "post", "message": message})
        )
        print("info No.3")

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
            print("connect No.1")
            session_id = self.scope["cookies"]["sessionid"]
            user = await get_user(session_id)
            # user =
            # user = await get_user(self.scope)
            print("connect No.2")
            # user = self.scope["user"]

            if user.is_authenticated:
                group_name = self.room_group_name + str(user.id)
                print(f"connect No.5:{user.id=}")
                await self.channel_layer.group_add(group_name, self.channel_name)
                # await self.channel_layer.group_add(
                #    self.tmp_group_name, self.channel_name
                # )
                print("connect No.6")

                await self.accept()  # WebSocket接続を受け入れる
                await update_user_login_state(user, True)
                # await self.send(text_data="message")
                # await self.send(text_data=json.dumps({"message": "test-message"}))
                # await self.channel_layer.group_send(
                #    group_name,
                #    {
                #        "type": "post",
                #        "message": "text_data33333",
                #        "param1": "param1",
                #        "param2": "param2",
                #        "param3": "param3",
                #        "param4": "",
                #    },
                # )
                print("connect No.7")
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
        # session_id = self.scope["cookies"]["sessionid"]
        session_id = self.scope["cookies"]["sessionid"]
        print("websocket_disconnect No.2")
        user = await get_user(session_id)

        # user = self.scope["user"]
        print(f"websocket_disconnect No.3 {user.id=}")
        await update_user_login_state(user, False)

        group_name = self.room_group_name + str(user.id)
        print(f"websocket_disconnect No.4 {group_name=}")
        print("websocket_disconnect No.5")
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
        print("websocket_disconnect No.6")

        print(message)
        pass

    # async def disconnect(self, close_code):
    #    print("disconect No.1")
    #    try:
    #        print("disconect No.2")
    #        session_id = self.scope["cookies"]["sessionid"]
    #        user = await get_user(session_id)
    #        # user = self.scope["user"]
    #        await update_user_login_state(user, False)
    #    except Exception:
    #        print("disconnect Exception Error")

    async def handle_post_method(self, user, json):
        print("handle_post_method No.1")
        if json["message"] == "active":
            print("handle_post_method No.2")
            await update_user_login_state(user, True)
            # await post.active(user, json)

    async def handle_get_method(self, user, json):
        message = ""
        print(f'{json["message"]=}')
        if json["message"] == "active_list":
            (message, param1, param2, param3, param4) = await get.active(json)

        group_name = self.room_group_name + str(user.id)
        if message == "":
            return
        print("send")
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
        print("send No.2")

    async def receive(self, text_data):
        session_id = self.scope["cookies"]["sessionid"]
        user = await get_user(session_id)
        if user.is_authenticated is False:
            return

        # WebSocketでメッセージを受信したときに呼ばれる
        # message = text_data_json["message"]

        try:
            text_data_json = json.loads(text_data)
            print(f"receie No.2:{text_data_json=}")
            message_type = text_data_json["type"]
            if message_type == "get":
                print("get type")
                await self.handle_get_method(user, text_data_json)
            elif message_type == "post":
                print("post type")
                await self.handle_post_method(user, text_data_json)
        except Exception as e:
            print(f"Websocket Error:{e}")

        # if message_type == "chat":
        #    print("receive Chat message")
        # elif message_type == "response":
        #    if message == "active":
        #        print("active")
        #        await update_user_login_state(user, True)
        # elif message_type == "connect":
        #    print("receive Connect message")

        #    group_name = self.room_group_name + str(user.id)
        #    await self.channel_layer.group_send(
        #        # await async_to_sync(self.channel_layer.group_send)(
        #        group_name,  # グループ名
        #        {
        #            "type": "info",  # イベントタイプ
        #            "message": "text_data",
        #            # "user_id": user.id,
        #            # "status": "online",  # 状態
        #        },
        #    )

        #    # content = text_data_json["content"]
        #    await update_user_login_state(user, True)
        print("receive end")

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
