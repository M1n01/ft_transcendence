from django.conf import settings
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponse,
)
from django.urls import reverse_lazy

from accounts.models import FtUser
from .forms import SignUpForm
from .oauth import FtOAuth, randomStr

from io import BytesIO
import qrcode
import qrcode.image.svg
import base64
import json
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class LoginFrom(AuthenticationForm):
    class Meta:
        model = FtUser


def make_qr(url):
    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer)
    return base64.b64encode(buffer.getvalue()).decode().replace("'", "")


class UserLogin(LoginView):
    ft_oauth = FtOAuth()
    url = ft_oauth.get_ft_authorization_url()
    form_class = LoginFrom
    template_name = "accounts/login.html"
    success_url = reverse_lazy("accounts:success-login")

    # QRコード作成
    try:
        qr = make_qr(url)
        extra_context = {"qr": qr, "ft_url": url}
    except:
        logger.error(f"QRコードの作成に失敗しました")
        error_page = getattr(settings, "ERROR_PAGE", None)
        qr = make_qr(error_page)
        extra_context = {"qr": "qr", "ft_url": url}


class UserLogout(LogoutView):
    redirect_field_name = "redirect"
    success_url = reverse_lazy("accounts:success-logout")


class SignupView(CreateView):

    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:success-signup")

    def form_valid(self, form):
        """
        CreateViewのメソッドをオーバーライド
        """
        try:
            response = super().form_valid(form)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return response
        except:
            return HttpResponseBadRequest("Bad Request")


def SignupSuccess(request):
    return render(request, "accounts/success-signup.html")


def LoginSuccess(request):
    return render(request, "accounts/success-login.html")


def LogoutSuccess(request):
    return render(request, "accounts/success-logout.html")


def oauth_login(request):
    """
    42OAuthのログインに利用する
    正確には、これを送信したクライアントが42認可サーバーに許可したかどうかを確認する
    引数のrequest内にあるurlにはstateとcodeの2つがあり、
    stateはバックエンド(Django)が作成したランダムな文字列
    codeは42の認可サーバーが作成したもの(リダイレクト時にDjangoにわたされる)
    この２つがマッチしていればこれを送信したクライアントが42認可サーバーに対して許可したことがわかる
    さらにこれらを42認可サーバーに渡すことでaccess_tokenを得ることができる
    このtokenによって、ユーザーの情報(username, email)を42から得ることができるので、
    これをDBに登録する


    引数:
        request:    ブラウザからのリクエストデータ
                    Postデータとして"url"を含まなければならない
    戻り値:
        Response:   クライアントに返すレスポンスデータ
    """
    ft_oauth = FtOAuth()
    try:
        # クライアントから42認可サーバーのURIを受け取る（そこにstatuとcodeが入っている)
        body = json.loads(request.body)
        url = body["url"]
        token_response = ft_oauth.send_ft_authorization(url)
        if token_response is None:
            return HttpResponseBadRequest("Bad Request")

        token_json = token_response.json()
        access_token = token_json["access_token"]
        user_response = ft_oauth.fetch_user(access_token)
        username = user_response["login"]
        email = user_response["email"]
        user = authenticate(request, username=username, email=email)

        if user is None:
            logger.error(f"failure to authenticate")
            return HttpResponseServerError("failure to authenticate")

        login(request, user, backend="accounts.oauth.FtOAuth")
        return HttpResponse()
    except RuntimeError as e:
        return HttpResponseServerError("failure to login")
    except ValueError as e:
        return HttpResponseBadRequest("Bad Request")
    except:
        return HttpResponseBadRequest("Bad Request")


class FtLoginFrom(AuthenticationForm):
    class Meta:
        model = FtUser


def redirect_oauth(request):
    """
    ユーザーが42認可サーバーに許可を出したときのリダイレクト先
    引数:
        request:    ブラウザからのリクエストデータ
                    クエリ内に、'code', 'state'を含んでいる
    戻り値:
        Response:   クライアントに返すレスポンスデータ
    """
    try:
        code = request.GET.get("code")
        state = request.GET.get("state")
        ft_oauth = FtOAuth()
        ft_oauth.append_state_code_dict(state, code)
        return render(request, "accounts/redirect-oauth.html")
    except:
        return HttpResponseBadRequest("Bad Request")
