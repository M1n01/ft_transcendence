from django.conf import settings
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView

# from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth.forms import AuthenticationForm
# from django.template.exceptions import TemplateDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required
from django.db import IntegrityError
from .models import FtTmpUser
from datetime import datetime, timezone, timedelta

# from .forms import FtLoginForm

# from django import forms
from django.views.generic import TemplateView

# from django.utils.translation import gettext_lazy as _

# from django.contrib.auth.models import User

# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import logout
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponseForbidden,
    HttpResponse,
)
from django.urls import reverse_lazy

# from phonenumbers import COUNTRY_CODE_TO_REGION_CODE

from accounts.models import FtUser

# from accounts.models import FtTmpUser
from accounts.two_fa import TwoFA

# from .forms import SignUpForm, SignUpTmpForm, LoginForm
from .forms import SignUpForm, LoginForm
from .oauth import FtOAuth

from io import BytesIO
import qrcode
import qrcode.image.svg
import base64
import json
import logging

# from django.contrib.auth import login as auth_login
# from django.template.loader import render_to_string
import secrets
from accounts.models import AuthChoices
from .backend import TmpUserBackend


def generate_secure_random_number():
    return secrets.randbelow(900000) + 100000  # 100000から999999の範囲の数値を生成


logger = logging.getLogger(__name__)


def make_qr(url):
    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer)
    return base64.b64encode(buffer.getvalue()).decode().replace("'", "")


def verify_two_fa(user, code, request):

    if user is None:
        return False
    if code is None or code == "":
        return False
    two_fa_mode = user.auth
    two_fa = TwoFA()
    if two_fa_mode == AuthChoices.SMS:
        rval = two_fa.verify_sms(user, code)
    elif two_fa_mode == AuthChoices.EMAIL:
        time = datetime.fromtimestamp(float(request.session["exp"]), tz=timezone.utc)
        rval = two_fa.verify_email(user, time, code)
    elif two_fa_mode == AuthChoices.APP:
        rval = two_fa.verify_app(user, code)
    return rval


def send_two_fa(user, request):
    try:
        two_fa_mode = user.auth
        two_fa = TwoFA()
        if two_fa_mode == AuthChoices.SMS:
            rval = two_fa.sms(user)
        elif two_fa_mode == AuthChoices.EMAIL:
            time = datetime.fromtimestamp(
                float(request.session["exp"]), tz=timezone.utc
            )
            rval = two_fa.email(user, time)
        elif two_fa_mode == AuthChoices.APP:
            rval = two_fa.app(user)
        return rval
    except Exception as e:
        print(f"{e=}")
        return False


def copy_tmpuser_to_ftuser(user):
    try:
        # new_user = FtUser()
        src_user = FtTmpUser.objects.get(email=user.email)
        FtUser.objects.create(
            username=src_user.username,
            password=src_user.password,
            email=src_user.email,
            email42=src_user.email42,
            first_name=src_user.first_name,
            last_name=src_user.last_name,
            country_code=src_user.country_code,
            phone=src_user.phone,
            is_ft=src_user.is_ft,
            is_active=src_user.is_active,
            birth_date=src_user.birth_date,
            auth=src_user.auth,
            app_secret=src_user.app_secret,
            last_login=src_user.last_login,
            created_at=src_user.created_at,
            is_superuser=src_user.is_superuser,
            is_staff=src_user.is_staff,
            language=src_user.language,
        )
    except IntegrityError as e:
        print(f"Copy Error:{e}")
    except Exception as e:
        print(f"Copy Error:{e}")


@method_decorator(login_not_required, name="dispatch")
class SignupTwoFaView(CreateView):
    def post(self, request):

        # if request.method == "POST":
        is_provisional_signup = False
        if "is_provisional_signup" in request.session:
            is_provisional_signup = request.session["is_provisional_signup"]
        if is_provisional_signup is False:
            return HttpResponseForbidden()
        try:
            id = request.session["user_id"]
            user = FtTmpUser.objects.get(id=id)
            if user is None:
                return HttpResponseServerError("User not Found")

            code = request.POST.get("code")
            rval = verify_two_fa(user, code, request)

            if rval is False:
                return HttpResponseBadRequest("Failure to verify")
            copy_tmpuser_to_ftuser(user)

            new_user = FtUser.objects.get(email=user.email)
            login(
                request,
                new_user,
                backend="django.contrib.auth.backends.ModelBackend",
            )

            tmp_time = datetime.now(tz=timezone.utc) + timedelta(
                seconds=getattr(settings, "JWT_VALID_TIME", None)
            )
            request.session["exp"] = str(tmp_time.timestamp())  # 5minutes
            return HttpResponse()

        except json.JSONDecodeError:
            return HttpResponseServerError("Server Error")

    # else:
    # return HttpResponseBadRequest("Bad Request")


@login_not_required
def two_fa_verify(request):
    if request.method == "POST":
        try:

            is_provisional_login = False
            user_id = ""
            if "is_provisional_login" in request.session:
                is_provisional_login = request.session["is_provisional_login"]
            if "user_id" in request.session:
                user_id = request.session["user_id"]
            if is_provisional_login is False or user_id == "":
                return HttpResponseForbidden()
            user = FtUser.objects.get(id=user_id)
            code = request.POST.get("code")
            rval = verify_two_fa(user, code, request)
            if rval is True:
                new_user = FtUser.objects.get(email=user.email)
                login(
                    request,
                    new_user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                tmp_time = datetime.now(tz=timezone.utc) + timedelta(
                    seconds=getattr(settings, "JWT_VALID_TIME", None)
                )
                request.session["exp"] = str(tmp_time.timestamp())  # 5minutes

                return HttpResponse()
            return HttpResponseBadRequest("Failure to verify")

        except json.JSONDecodeError:
            return HttpResponseServerError("Server Error")
    else:
        return HttpResponseBadRequest("Bad Request")


@method_decorator(login_not_required, name="dispatch")
class LoginSignupView(TemplateView):
    ft_oauth = FtOAuth()
    url = ft_oauth.get_ft_authorization_url()
    # template_name = "login-signup.html"
    # template_name = "login.html"
    template_name = "accounts/login-signup.html"
    signup_form = SignUpForm
    login_form = LoginForm

    # QRコード作成
    try:
        qr = make_qr(url)
        extra_context = {
            "qr": qr,
            "ft_url": url,
            "signup_form": signup_form,
            "login_form": login_form,
        }
    except Exception as e:
        logger.error(f"QRコードの作成に失敗しました:{e}")
        error_page = getattr(settings, "ERROR_PAGE", None)
        qr = make_qr(error_page)
        extra_context = {
            "qr": "qr",
            "ft_url": url,
            "signup_form": signup_form,
            "login_form": login_form,
        }

    def get(self, request):
        return render(
            request,
            "accounts/login-signup.html",
            self.extra_context,
        )


@method_decorator(login_not_required, name="dispatch")
class UserLoginView(LoginView):
    ft_oauth = FtOAuth()
    url = ft_oauth.get_ft_authorization_url()
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("accounts:two-fa")

    # QRコード作成
    try:
        qr = make_qr(url)
        extra_context = {"qr": qr, "ft_url": url}
    except Exception as e:
        logger.error(f"QRコードの作成に失敗しました:{e}")
        error_page = getattr(settings, "ERROR_PAGE", None)
        qr = make_qr(error_page)
        extra_context = {"qr": "qr", "ft_url": url}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def form_valid(self, form):
        """
        Login認証が成功時の戻り値をオーバーライド
        """

        try:
            if self.request.method != "POST":
                return HttpResponseBadRequest("Bad Request")

            username = self.request.POST.get("username")
            password = self.request.POST.get("password")
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                print("User is None")
                return HttpResponseServerError("Bad Request")

            tmp_time = datetime.now(tz=timezone.utc) + timedelta(seconds=300)
            self.request.session["exp"] = str(tmp_time.timestamp())  # 5minutes
            self.request.session["is_provisional_login"] = True
            self.request.session["user_id"] = user.id
            rval = send_two_fa(user, self.request)
            if rval:
                is_app = user.auth == AuthChoices.APP
                data = {"is_auth_app": is_app}
                return JsonResponse(data)
            else:
                self.request.session["is_provisional_login"] = False
                self.request.session["user_id"] = 0

        except Exception as e:
            return HttpResponseBadRequest(f"Bad Request:{e}")
        return HttpResponseBadRequest("Bad Request")

    def form_invalid(self, form):
        """
        Login認証が失敗時の戻り値をオーバーライド
        現在は特に変更する必要がないので、そのまま返す
        """
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class UserLogout(LogoutView):
    redirect_field_name = "redirect"
    success_url = reverse_lazy("spa:top")


@method_decorator(login_not_required, name="dispatch")
class SignupView(CreateView):
    """
    Signupフォームを送信されたときに実行される
    フォームのバリデーションを実行し、DBにユーザーを仮登録し、
    2FAを指定されたデバイスに送信(Appは除く)
    """

    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("spa:top")
    usable_password = None

    def form_invalid(self, form):
        # ここでエラーメッセージを追加したり、カスタマイズしたりできる
        # form.add_error(None, "全体に関するエラーメッセージを追加することができます。")
        res = super().form_invalid(form)
        res.status_code = 400
        return res

    def form_valid(self, form):
        try:
            form = SignUpForm(self.request.POST)
            tmp_res = super().form_valid(form)
            if tmp_res.status_code >= 300 and tmp_res.status_code < 400:
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password1"]
                backend = TmpUserBackend()
                user = backend.authenticate(
                    self.request, email=email, password=password
                )
                if user is None:
                    return HttpResponseServerError("Server Error")
                tmp_time = datetime.now(tz=timezone.utc) + timedelta(
                    seconds=getattr(settings, "JWT_TMP_VALID_TIME", None)
                )
                self.request.session["exp"] = str(tmp_time.timestamp())  # 5minutes
                self.request.session["is_provisional_signup"] = True
                self.request.session["user_id"] = user.id

                rval = send_two_fa(user, self.request)
                if rval is False:
                    return HttpResponseServerError("Bad Request")
                two_fa_mode = user.auth
                data = {"valid": True, "is_auth_app": False}
                if two_fa_mode == AuthChoices.SMS:
                    data = {"valid": True, "is_auth_app": False}
                elif two_fa_mode == AuthChoices.EMAIL:
                    data = {"valid": True, "is_auth_app": False}
                elif two_fa_mode == AuthChoices.APP:
                    data = {"valid": True, "is_auth_app": True, "qr": make_qr(rval)}

                return JsonResponse(data)
            else:

                tmp_res.status_code = 400
                return tmp_res
        except Exception as e:
            print(f"{e=}")
            return HttpResponseServerError(f"Server Error:{e}")


@login_not_required
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
            logger.error("failure to authenticate")
            return HttpResponseServerError("failure to authenticate")
        login(request, user, backend="accounts.oauth.FtOAuth")
        tmp_time = datetime.now(tz=timezone.utc) + timedelta(
            seconds=getattr(settings, "JWT_VALID_TIME", None)
        )
        request.session["exp"] = str(tmp_time.timestamp())  # 5minutes

        return HttpResponse()
    except RuntimeError as e:
        return HttpResponseServerError("failure to login:" + e)
    except ValueError as e:
        return HttpResponseBadRequest("Bad Request:" + e)
    except Exception as e:
        return HttpResponseBadRequest("Bad Request:" + e)


@login_not_required
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
    except Exception as e:
        return HttpResponseBadRequest(f"Bad Request:{e}")


@method_decorator(login_not_required, name="dispatch")
class LoginTwoFaView(TemplateView):
    """
    2認証のモードとその値を元に、認証サービスにデータを送信する
    引数:
        request:    ブラウザからのリクエストデータ
    戻り値:
        Response:   クライアントに返すレスポンスデータ
    """

    def post(self, request):
        try:

            is_provisional_login = False
            user_id = ""
            if "is_provisional_login" in request.session:
                is_provisional_login = request.session["is_provisional_login"]
            if "user_id" in request.session:
                user_id = request.session["user_id"]
            if is_provisional_login is False or user_id == "":
                return HttpResponseForbidden()
            user = FtUser.objects.get(id=user_id)
            code = request.POST.get("code")
            rval = verify_two_fa(user, code, request)
            if rval is True:
                new_user = FtUser.objects.get(email=user.email)
                login(
                    request,
                    new_user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                tmp_time = datetime.now(tz=timezone.utc) + timedelta(
                    seconds=getattr(settings, "JWT_VALID_TIME", None)
                )
                request.session["exp"] = str(tmp_time.timestamp())  # 5minutes
                return HttpResponse()
            return HttpResponseBadRequest("Failure to verify")

        except json.JSONDecodeError:
            return HttpResponseServerError("Server Error")
