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
    """
    ランダムな文字列を返す
    引数:
        n:      文字数
    戻り値:
        string: n文字数なランダムな文字列
    """
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return "".join(randlst)


def query_to_dict(url):
    """
    urlのクエリをdictに変換して返す
    引数:
        url:    対象のurl文字列
    戻り値:
        Dict: urlから抽出したクエリを辞書型に変換したもの
    """
    parsed_url = urlparse(url)
    query_dict = parse_qs(parsed_url.query)
    return query_dict


# 42認可サーバーから受け取る、state,codeの組み合わせをdictで管理
state_code_dict = {}


class FtOAuth(ModelBackend):
    """
    FtUser用の認証バックエンドクラス
    """

    BASE_URL = getattr(settings, "OAUTH_AUTHORIZE_URL", None)
    CLIENT_ID = getattr(settings, "OAUTH_CLIENT_ID", None)
    SECRET_ID = getattr(settings, "OAUTH_SECRET_ID", None)
    DOMAIN = getattr(settings, "PONG_DOMAIN", None)
    REDIRECTED_URL = DOMAIN + "accounts/redirect-oauth"

    def authenticate(self, username, email):
        try:
            user = FtUser.objects.get(email42=email)
        except FtUser.DoesNotExist:
            user = FtUser()
            cnt = 0
            try:
                cnt = FtUser.objects.count()
            except:
                cnt = 0
            user.username = username
            user.email = str(cnt) + email  # dummy email
            user.email42 = email
            user.password = randomStr(32)
            user.created_at = datetime.datetime.now()
            user.save()
            user = FtUser.objects.get(email42=email)
        return user

    def append_state_code_dict(self, state, code):
        state_code_dict[state] = code

    def get_ft_authorization_url(self):
        """
        42認可サーバーのURL取得
        """
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

    def fetch_user(self, access_token):
        """
        42認可サーバーからユーザー情報を取得

        引数:
            access_token: 42のaccess_token
        戻り値:
            json: ユーザー情報
        """
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
