from django.conf import settings
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView

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
from .forms import SignUpTmpForm, LoginForm
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
        time = datetime.fromtimestamp(float(request.session["exp"]))
        rval = two_fa.verify_email(user, time, code)
    elif two_fa_mode == AuthChoices.APP:
        rval = two_fa.verify_app(user, code)
    return rval


# def send_two_fa_view(request):
#    user = request.user
#    rval = send_two_fa(user, request)
#    if rval is False:
#        return HttpResponseServerError()
#    return HttpResponse()


def send_two_fa(user, request):
    try:
        two_fa_mode = user.auth
        two_fa = TwoFA()
        if two_fa_mode == AuthChoices.SMS:
            rval = two_fa.sms(user)
        elif two_fa_mode == AuthChoices.EMAIL:
            time = datetime.fromtimestamp(float(request.session["exp"]))
            rval = two_fa.email(user, time)
        elif two_fa_mode == AuthChoices.APP:
            rval = two_fa.app(user)
        return rval
    except Exception as e:
        print(f"{e=}")
        return False


# def send_two_fa_with_form(form):
#    try:
#        two_fa_mode = form.cleaned_data["auth"]
#        email = form.cleaned_data["email"]
#        user = FtUser.objects.get(email=email)
#        two_fa = TwoFA()
#        if two_fa_mode == AuthChoices.SMS:
#            rval = two_fa.sms(user)
#        elif two_fa_mode == AuthChoices.EMAIL:
#            email = form.cleaned_data["email"]
#            rval = two_fa.email(user)
#        elif two_fa_mode == AuthChoices.APP:
#            # two_fa.make_qr(user)
#            rval = two_fa.app(user)
#        return rval
#    except Exception as e:
#        print(f"{e=}")
#        return False


# class UserTmpLogin(LoginView):
#    form = FtLoginForm
#
#    def form_invalid(self, form):
#        return HttpResponseBadRequest("Bad Request")
#
#    def form_valid(self, form):
#        """
#        Login認証が成功時の戻り値をオーバーライド
#        """
#
#        """Security check complete. Log the user in."""
#        try:
#            if self.request.method != "POST":
#                return HttpResponseBadRequest("Bad Request")
#            username = self.request.POST.get("username")
#            password = self.request.POST.get("password")
#            user = authenticate(self.request, username=username, password=password)
#            if user is None:
#                return HttpResponseBadRequest("Bad Request")
#            rval = send_two_fa(user, self.request)
#            if rval:
#                self.request.session["is_provisional_login"] = True
#                self.request.session["user_id"] = user.id
#                return HttpResponse()
#        except TemplateDoesNotExist as e:
#            return HttpResponseBadRequest(f"Bad Request:{e}")
#        except Exception as e:
#            return HttpResponseBadRequest(f"Bad Request:{e}")
#        else:
#            return HttpResponseBadRequest("Bad Request")


@login_not_required
def signup_two_fa(request):

    if request.method == "GET":
        return HttpResponseBadRequest()
    elif request.method == "POST":
        is_provisional_login = False
        if "is_provisional_login" in request.session:
            is_provisional_login = request.session["is_provisional_login"]
        if is_provisional_login is False:
            return HttpResponseForbidden()

        # pass
        # elif request.method == "GET":
        try:
            id = request.session["user_id"]
            user = FtTmpUser.objects.get(id=id)
            # user = request.user
            two_fa_mode = user.auth
            # rval = send_two_fa(request)

            rval = send_two_fa(user, request)
            if rval is False:
                return HttpResponseServerError("Bad Request")
            two_fa_mode = user.auth
            data = {"valid": True, "is_auth_app": False}
            if two_fa_mode == AuthChoices.APP:
                data = {"valid": True, "is_auth_app": True, "qr": make_qr(rval)}
            return JsonResponse(data)

        except Exception as e:
            return HttpResponseServerError(f"Bad Request:{e}")


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


@login_not_required
def signup_two_fa_verify(request):

    is_provisional_login = False
    if "is_provisional_login" in request.session:
        is_provisional_login = request.session["is_provisional_login"]
    if is_provisional_login is False:
        return HttpResponseForbidden()

    if request.method == "POST":
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

            # new_user = authenticate(
            # request, username=user.email, password=test_user.password
            # )
            # if new_user is None:
            # else:
            # print("New User Exist")
            new_user = FtUser.objects.get(email=user.email)
            # src_user = FtTmpUser.objects.get(email=user.email)
            login(
                request,
                new_user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            return HttpResponse()

        except json.JSONDecodeError:
            return HttpResponseServerError("Server Error")
            return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")


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

            # user = request.user
            code = request.POST.get("code")
            # rval = False

            rval = verify_two_fa(user, code, request)

            if rval is True:

                new_user = FtUser.objects.get(email=user.email)
                # src_user = FtTmpUser.objects.get(email=user.email)
                login(
                    request,
                    new_user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                # return HttpResponse()
                return render(request, "accounts/success-login.html")
            return HttpResponseBadRequest("Failure to verify")

        except json.JSONDecodeError:
            return HttpResponseServerError("Server Error")
            return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")


@method_decorator(login_not_required, name="dispatch")
class LoginSignupView(TemplateView):
    ft_oauth = FtOAuth()
    url = ft_oauth.get_ft_authorization_url()
    # template_name = "login-signup.html"
    # template_name = "login.html"
    template_name = "accounts/login-signup.html"
    signup_form = SignUpTmpForm
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
        # form = SignUpTmpForm
        # form = MyForm()
        return render(
            request,
            "accounts/login-signup.html",
            self.extra_context,
            # {"signup_form": self.signup_form, "login_form": self.login_form},
        )


@method_decorator(login_not_required, name="dispatch")
class UserLogin(LoginView):
    ft_oauth = FtOAuth()
    # ft_oauth = TmpUserBackend()
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

    # Get Method
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # if "is_2fa" in request.session:
        #    context["is_2fa"] = request.session["is_2fa"]
        # else:
        #    context["is_2fa"] = False
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
            # code = self.request.POST.get("code")
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                print("User is None")
                return HttpResponseServerError("Bad Request")

            # rval = verify_two_fa(user, code)
            tmp_time = datetime.now(tz=timezone.utc) + timedelta(seconds=300)
            self.request.session["exp"] = str(tmp_time.timestamp())  # 5minutes
            self.request.session["is_provisional_login"] = True
            self.request.session["user_id"] = user.id
            rval = send_two_fa(user, self.request)
            if rval:
                # auth_login(self.request, form.get_user())
                is_app = user.auth == AuthChoices.APP
                data = {"is_auth_app": is_app}

                # if is_app:
                #    data = {"is_auth_app": True, "qr": make_qr(rval)}
                # else:
                #    data = {"is_auth_app": is_app}

                return JsonResponse(data)
            else:
                self.request.session["is_provisional_login"] = False
                self.request.session["user_id"] = 0
                # return render(self.request, "accounts/two-fa.html", context=data)

            """Security check complete. Log the user in."""
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
    # success_url = reverse_lazy("accounts:success-logout")
    success_url = reverse_lazy("spa:index")

    def post(self, request, *args, **kwargs):
        # request.session["is_2fa"] = False
        return super().post(request, *args, **kwargs)


@method_decorator(login_not_required, name="dispatch")
class SignupView(CreateView):

    form_class = SignUpTmpForm
    template_name = "accounts/signup.html"
    # success_url = reverse_lazy("accounts:success-signup")
    success_url = reverse_lazy("spa:index")

    # cnt = "0-"
    # try:
    #    cnt = FtUser.objects.count() + "-"
    # except:
    #    cnt = "0-"
    # extra_context = {"dummy_email": cnt + randomStr(64) + "@" + randomStr(16) + ".com"}

    def form_invalid(self, form):
        print("form_invalid No.1")
        # ここでエラーメッセージを追加したり、カスタマイズしたりできる
        # form.add_error(None, "全体に関するエラーメッセージを追加することができます。")
        res = super().form_invalid(form)
        res.status_code = 400
        # print("form_invalid No.2")
        # print(f"{res.content=}")
        # body_bytes = res.content  # バイト形式のボディ
        # body_str = body_bytes.decode("utf-8")  # UTF-8としてデコードして文字列に変換

        # デバッグまたは他の処理に使用する
        # print(f"{body_str=}")  # 例: レスポンスボディを出力
        # print("form_invalid No.3")
        return res

    def form_valid(self, form):
        try:
            form = SignUpTmpForm(self.request.POST)
            tmp_res = super().form_valid(form)
            if tmp_res.status_code >= 300 and tmp_res.status_code < 400:
                form.save()

                email = form.cleaned_data["email"]
                password = form.cleaned_data["password1"]
                # user = FtTmpUser.objects.get(email=email)
                backend = TmpUserBackend()
                user = backend.authenticate(
                    self.request, email=email, password=password
                )
                if user is None:
                    return HttpResponseServerError("Server Error")
                tmp_time = datetime.now(tz=timezone.utc) + timedelta(seconds=300)
                self.request.session["exp"] = str(tmp_time.timestamp())  # 5minutes
                self.request.session["is_provisional_login"] = True
                self.request.session["user_id"] = user.id

                # url = "accounts/signup-two-fa.html"
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
                # return JsonResponse(data)
        except Exception as e:
            print(f"{e=}")
            return HttpResponseServerError(f"Server Error:{e}")


# @login_not_required
# def signup_valid(request):
#    if request.method == "POST":
#        try:
#            form = SignUpTmpForm(request.POST)
#            if form.is_valid():
#                tmp_form = SignUpTmpForm(request.POST)
#
#                tmp_form.save()
#
#                email = form.cleaned_data["email"]
#                password = form.cleaned_data["password1"]
#                # user = FtTmpUser.objects.get(email=email)
#                backend = TmpUserBackend()
#                user = backend.authenticate(request, email=email, password=password)
#                if user is None:
#                    return HttpResponseServerError("Server Error")
#                # login(
#                #    request,
#                #    user,
#                #    backend="accounts.backend.TmpUserBackend",
#                # )
#
#                # url = "accounts/signup-two-fa.html"
#                rval = send_two_fa(user, request)
#                if rval is False:
#                    return HttpResponseServerError("Bad Request")
#                two_fa_mode = user.auth
#                data = {"valid": True, "is_auth_app": False}
#                if two_fa_mode == AuthChoices.SMS:
#                    html = render_to_string(
#                        "accounts/signup-two-fa.html", request=request
#                    )
#                elif two_fa_mode == AuthChoices.EMAIL:
#                    html = render_to_string(
#                        "accounts/signup-two-fa.html", request=request
#                    )
#                elif two_fa_mode == AuthChoices.APP:
#                    data = {"valid": True, "is_auth_app": True, "qr": make_qr(rval)}
#                request.session["is_provisional_login"] = True
#                request.session["user_id"] = user.id
#                tmp_time = datetime.now(tz=timezone.utc) + timedelta(seconds=300)
#                request.session["exp"] = str(tmp_time.timestamp())  # 5minutes
#                return JsonResponse(data)
#            else:
#                html = render_to_string(
#                    "accounts/signup.html", {"form": form}, request=request
#                )
#
#                data = {"valid": False, "html": html}
#                return JsonResponse(data)
#        except Exception as e:
#            return HttpResponseServerError(f"Server Error:{e}")
#    return HttpResponseBadRequest("Bad Request")


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


@login_not_required
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

            is_provisional_login = False
            user_id = ""

            if "is_provisional_login" in request.session:
                is_provisional_login = request.session["is_provisional_login"]
            if "user_id" in request.session:
                user_id = request.session["user_id"]
            if is_provisional_login is False or user_id == "":
                return HttpResponseForbidden()
            # return HttpResponseForbidden()
            user = FtUser.objects.get(id=user_id)
            if user is None:
                return HttpResponseServerError()

            mode = user.auth
            if mode == "EMAIL":
                # email_address = request.POST.get("id")
                # user = FtUser.objects.get(email=email_address)
                twilio = TwoFA()
                time = datetime.fromtimestamp(float(request.session["exp"]))
                rval = twilio.email(user, time)
                if rval:
                    extra_context = {"app": False}
                    return JsonResponse(extra_context)
            elif mode == "SMS":
                # phone_number = request.POST.get("id")
                twilio = TwoFA()
                rval = twilio.sms(user)
                if rval:
                    extra_context = {"app": False}
                    return JsonResponse(extra_context)
            elif mode == "APP":
                twilio = TwoFA()
                uri = twilio.app(user)
                qr = make_qr(uri)
                extra_context = {"app": True, "qr": qr}
                return JsonResponse(extra_context)

            return HttpResponseBadRequest("Bad Request")

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")
