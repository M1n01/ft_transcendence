from django.conf import settings
import urllib.parse
import random, string
import requests
import json
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.backends import BaseBackend, ModelBackend, RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware
import datetime
import logging

# from .modelss import User, FtUser
from .models import FtUser

logger = logging.getLogger(__name__)


def randomStr(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return "".join(randlst)


def query_to_dict(url):
    parsed_url = urlparse(url)
    query_dict = parse_qs(parsed_url.query)
    return query_dict


"""
class LoginIdModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            login_id = kwargs.get("login_id")
            if not login_id:
                raise User.DoesNotExist
            user = User.objects.get(login_id=login_id)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
"""

# 42認可サーバーから受け取る、state,codeの組み合わせをdictで管理
state_code_dict = {}

# class CustomHeaderMiddleware(RemoteUserMiddleware):
# header = "HTTP_AUTHUSER"


# class FtOAuth(RemoteUserBackend):
class FtOAuth(ModelBackend):
    # class FtOAuth(BaseBackend):
    # class FtOAuth:
    BASE_URL = getattr(settings, "OAUTH_AUTHORIZE_URL", None)
    CLIENT_ID = getattr(settings, "OAUTH_CLIENT_ID", None)
    SECRET_ID = getattr(settings, "OAUTH_SECRET_ID", None)
    DOMAIN = getattr(settings, "PONG_DOMAIN", None)
    REDIRECTED_URL = DOMAIN + "accounts/redirect-oauth"

    def authenticate(self, request, username, email):
        try:
            print("FtOAuth authenticate No.2")
            user = FtUser.objects.get(username=username)
            print("FtOAuth authenticate No.3 username:" + user.username)
        except FtUser.DoesNotExist:
            print("Error")
            user = FtUser()
            user.username = username
            user.email = email
            user.password = randomStr(32)
            user.created_at = datetime.datetime.now()
            print("FtOAuth authenticate No.4")
            user.save()
            print("FtOAuth authenticate No.5")
            user = FtUser.objects.get(username=username)
            print("FtOAuth authenticate No.6")
            # user.email2 = email
            # raise exceptions.AuthenticationFailed("No such user")
        print("FtOAuth authenticate No.7")
        return user

    def append_state_code_dict(self, state, code):
        state_code_dict[state] = code

    # def make_user(self, state, code):
    # state_code_dict[state] = code
    # FtUser.a

    # 42認可サーバーのURL取得
    def get_ft_authorization_url(self):
        redirect_uri = self.REDIRECTED_URL
        query_list = {
            "client_id": self.CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "public",
            "state": randomStr(64),
        }
        # self.state_code_dict[query_list["state"]] = ""
        query = urllib.parse.urlencode(query_list)
        url = self.BASE_URL + "?" + query
        return url

    # curl -F grant_type=authorization_code -F client_id=u-s4t2ud-69852fb56c7eac30b2c17c5d17509527815e50bb2ce195c461931cff5ed594a7
    # -F client_secret=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
    # -F code=50917ac89e6661453c80947571cced5d0f62d192d08955937d34aa92a114fef9
    # -F redirect_uri=https://localhost/ -X POST https://api.intra.42.fr/oauth/token

    def receive_redirect(self, url):
        return url

    def fetch_user(self, access_token):
        url_user = "https://api.intra.42.fr/v2/me"
        headers = {
            "Authorization": "Bearer " + access_token,
        }
        response = requests.get(url_user, headers=headers)
        return response.json()

    def fetch_access_token(self, state, code):
        """
        必要なデータを収集して、
        42認可サーバーに送信してaccess_tokenを取得する

        引数:
            state:      Djangoが作成したランダムデータ
            code:       42認可サーバーが作成したランダムデータ
        戻り値:
            Response:   送信結果のレスポンスデータ
        """
        ft_oauth_url = "https://api.intra.42.fr/oauth/token"
        params = {
            "grant_type": "authorization_code",
            "client_id": self.CLIENT_ID,
            "client_secret": self.SECRET_ID,
            "code": code,
            "redirect_uri": self.REDIRECTED_URL,
            "state": state,
        }
        response = requests.post(ft_oauth_url, params=params)
        if response.status_code >= 400:
            logger.error(f"error:{response.status_code=}")
            raise RuntimeError(
                f"42認可サーバーに対する通信に失敗しました：{response.status_code}"
            )
        return response

    # 42認可サーバーへ送信
    def send_ft_authorization(self, url):
        """
        引数のurlからstateを抽出し、
        42認可サーバーに送信してaccess_tokenを取得する


        引数:
            request:    ブラウザからのリクエストデータ
                        クエリとして"state"と"code"を含まなければならない
        戻り値:
            Response:   送信結果のレスポンスデータ

        """
        query = query_to_dict(url)
        if "state" not in query:
            logger.error(f"not find state in query")
            raise ValueError("Requestされたデータは無効です")
        state = query["state"][0]
        if state not in state_code_dict:
            logger.error(f"not find state in state_code_dict")
            raise ValueError("Requestされたデータは無効です")

        code = state_code_dict[state]
        return self.fetch_access_token(state, code)
