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
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE

from accounts.models import FtUser
from accounts.two_fa import TwoFA
from .forms import SignUpForm
from .oauth import FtOAuth, randomStr

from io import BytesIO
import qrcode
import qrcode.image.svg
import base64
import json
import logging
import datetime
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django import forms
import jwt
import secrets


def generate_secure_random_number():
    return secrets.randbelow(900000) + 100000  # 100000から999999の範囲の数値を生成


logger = logging.getLogger(__name__)


# Create your views here.
class LoginFrom(AuthenticationForm):
    # username = forms.CharField(label="Email or Phone Number")
    #COUNTRY_CODE_CHOICES = [(f"+{code}", f"+{code} ({region[0]})") for code, region in COUNTRY_CODE_TO_REGION_CODE.items()]
    #country_code = forms.ChoiceField(choices=COUNTRY_CODE_CHOICES, label="Country Code")
    #phone_number = forms.CharField(max_length=15, label="Phone Number")

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
    success_url = reverse_lazy("accounts:two-fa")

    # QRコード作成
    try:
        qr = make_qr(url)
        extra_context = {"qr": qr, "ft_url": url}
    except:
        logger.error(f"QRコードの作成に失敗しました")
        error_page = getattr(settings, "ERROR_PAGE", None)
        qr = make_qr(error_page)
        extra_context = {"qr": "qr", "ft_url": url}

    # Get Method
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "is_2fa" in request.session:
            context["is_2fa"] = request.session["is_2fa"]
        else:
            context["is_2fa"] = False
        return self.render_to_response(context)

    def form_valid(self, form):
        """
        Login認証が成功時の戻り値をオーバーライド
        """

        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        # return HttpResponseRedirect(self.get_success_url())
        json = {
            "dispatchEvent": "TwoFaEvent",
            "html": "/2fa",
        }
        return JsonResponse(json)

    def form_invalid(self, form):
        """
        Login認証が失敗時の戻り値をオーバーライド
        現在は特に変更する必要がないので、そのまま返す
        """
        return super().form_invalid(form)


class UserLogout(LogoutView):
    redirect_field_name = "redirect"
    success_url = reverse_lazy("accounts:success-logout")

    def post(self, request, *args, **kwargs):
        request.session["is_2fa"] = False
        return super().post(request, *args, **kwargs)
        """Logout may be done via POST."""
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)


class SignupView(CreateView):

    form_class = SignUpForm
    template_name = "accounts/signup.html"
    # success_url = reverse_lazy("accounts:success-signup")
    success_url = reverse_lazy("accounts:two-fa")

    cnt = "0-"
    try:
        cnt = FtUser.objects.count() + "-"
    except:
        cnt = "0-"
    extra_context = {"dummy_email": cnt + randomStr(64) + "@" + randomStr(16) + ".com"}

    def form_valid(self, form):
        """
        CreateViewのメソッドをオーバーライド
        """
        try:
            print(f"{form=}")
            return super().form_valid(form)
        except Exception as e:
            return HttpResponseBadRequest("Bad Request:" + e)


def SignupSuccess(request):
    context = {}
    if "is_2fa" in request.session:
        context["is_2fa"] = request.session["is_2fa"]
    else:
        context["is_2fa"] = False
    # return render(request, "accounts/success-login.html", context)
    return render(request, "accounts/two-fa.html", context)


def LoginSuccess(request):
    context = {}
    if "is_2fa" in request.session:
        context["is_2fa"] = request.session["is_2fa"]
    else:
        context["is_2fa"] = False
    # return render(request, "accounts/success-login.html", context)
    return render(request, "accounts/two-fa.html", context)


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
        user = ft_oauth.authenticate(username=username, email=email)

        if user is None:
            logger.error(f"failure to authenticate")
            return HttpResponseServerError("failure to authenticate")
        login(request, user, backend="accounts.oauth.FtOAuth")
        return HttpResponse()
    except RuntimeError as e:
        return HttpResponseServerError("failure to login:" + e)
    except ValueError as e:
        return HttpResponseBadRequest("Bad Request:" + e)
    except Exception as e:
        return HttpResponseBadRequest("Bad Request:" + e)


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


def two_fa(request):
    """
    2認証のモードとその値を元に、認証サービスにデータを送信する
    引数:
        request:    ブラウザからのリクエストデータ
    戻り値:
        Response:   クライアントに返すレスポンスデータ
    """
    if request.method == "GET":
        return render(request, "accounts/two-fa.html")

    if request.method == "POST":
        try:
            mode = request.POST.get("mode")
            # body = json.loads(request.body)
            # mode = body["mode"]
            print(f"{mode=}")
            if mode == "email":
                email_address = request.POST.get("email")
                code = generate_secure_random_number()
                twilio = TwoFA()
                rval = twilio.email(email_address, code)
                print(f"{email_address=}")
                if rval:
                    return HttpResponse()
            elif mode == "sms":
                phone_number = request.POST.get("phone")
                twilio = TwoFA()
                rval = twilio.sms(phone_number)
                # rval = False
                print(f"{phone_number=}")

                # json = {
                # "page":"overwrite",
                # "dispatchEvent": "TwoFaEvent",
                # "data": "",
                # }
                if rval:
                    return HttpResponse()
                # return JsonResponse(json)
                # return render(request, "accounts/two-fa-sms.html")
            elif mode == "app":
                app_name = request.POST.get("app")
                print(f"{app_name=}")
            return HttpResponseBadRequest("Bad Request")

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Bad Request")
        # except RawPostDataException:
        # return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")


def two_fa_verify(request):
    if request.method == "POST":
        try:
            mode = request.POST.get("mode")
            pre_input = request.POST.get("pre_input")
            code = request.POST.get("code")
            print(f"{code=}")
            print(f"{pre_input=}")
            print(f"{mode=}")
            rval = False
            if mode == "email":
                print("email")
                twilio = TwoFA()
                rval = twilio.verify_email(pre_input, code)
                # return HttpResponse()
            elif mode == "sms":
                print("sms")
                twilio = TwoFA()
                rval = twilio.verify_sms(pre_input, code)
                # return HttpResponse()
                # rval = True
            elif mode == "app":
                print("app")
                return HttpResponse()
            if rval == True:
                request.session["is_2fa"] = True
                # tmp_session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
                print(f"test 2fa")
                # test = getattr(settings, "SECRET_KEY", None)
                # print(f"{test=}")
                # jwt_decode = jwt.decode(
                # tmp_session_key,
                # getattr(settings, "SECRET_KEY", None),
                # leeway=5,  # 通信上の遅延で５秒遅くても大丈夫ないように
                # algorithms=["HS256"],
                # )
                # jwt_decode["is_2fa"] = True
                # session_key = jwt.encode(jwt_decode)
                # request.set_cookie(settings.SESSION_COOKIE_NAME, session_key)
                # return JsonResponse(json)
                return render(request, "accounts/success-login.html")
            return HttpResponseBadRequest("Failure to verify")

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Bad Request")
        # except RawPostDataException:
        # return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")
