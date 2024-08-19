from django.conf import settings
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.template.exceptions import TemplateDoesNotExist

# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import logout
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponse,
)
from django.urls import reverse_lazy

# from phonenumbers import COUNTRY_CODE_TO_REGION_CODE

from accounts.models import FtUser

# from accounts.models import FtTmpUser
from accounts.two_fa import TwoFA
from .forms import SignUpForm
from .oauth import FtOAuth

from io import BytesIO
import qrcode
import qrcode.image.svg
import base64
import json
import logging
from django.contrib.auth import login as auth_login
from django.template.loader import render_to_string
import secrets
from accounts.models import AuthChoices


def generate_secure_random_number():
    return secrets.randbelow(900000) + 100000  # 100000から999999の範囲の数値を生成


logger = logging.getLogger(__name__)


class LoginFrom(AuthenticationForm):
    class Meta:
        model = FtUser


def make_qr(url):
    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer)
    return base64.b64encode(buffer.getvalue()).decode().replace("'", "")


def verify_two_fa(user, code):

    if user is None:
        return False
    if code is None or code == "":
        return False
    two_fa_mode = user.auth
    two_fa = TwoFA()
    if two_fa_mode == AuthChoices.SMS:
        # phone_number = user.phone
        phone_number = user.country_code + user.phone
        rval = two_fa.verify_sms(phone_number, code)
    elif two_fa_mode == AuthChoices.EMAIL:
        email = user.email
        rval = two_fa.verify_email(email, code)
    elif two_fa_mode == AuthChoices.APP:
        secret = user.app_secret
        rval = two_fa.verify_app(secret, code)
    return rval


def send_two_fa(user):
    try:
        two_fa_mode = user.auth
        two_fa = TwoFA()
        if two_fa_mode == AuthChoices.SMS:
            # phone_number = user.country_code
            phone_number = user.country_code + user.phone
            rval = two_fa.sms(phone_number)
        elif two_fa_mode == AuthChoices.EMAIL:
            code = generate_secure_random_number()
            email = user.email
            rval = two_fa.email(email, code)
        elif two_fa_mode == AuthChoices.APP:
            rval = two_fa.app()
        return rval
    except Exception as e:
        print(f"{e=}")
        return False


class UserTmpLogin(LoginView):
    def form_invalid(self, form):
        return HttpResponseBadRequest("Bad Request")

    def form_valid(self, form):
        """
        Login認証が成功時の戻り値をオーバーライド
        """

        """Security check complete. Log the user in."""
        try:
            if self.request.method != "POST":
                return HttpResponseBadRequest("Bad Request")
            username = self.request.POST.get("username")
            password = self.request.POST.get("password")
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                return HttpResponseBadRequest("Bad Request")
            rval = send_two_fa(user)
            if rval:
                return HttpResponse()
        except TemplateDoesNotExist as e:
            return HttpResponseBadRequest(f"Bad Request:{e}")
        except Exception as e:
            return HttpResponseBadRequest(f"Bad Request:{e}")
        else:
            return HttpResponseBadRequest("Bad Request")


def signup_two_fa_verify(request):
    if request.method == "POST":
        try:
            mode = request.POST.get("mode")
            pre_input = request.POST.get("id")
            code = request.POST.get("code")
            secret = request.POST.get("app_secret")
            rval = False
            if mode == "EMAIL":
                twilio = TwoFA()
                rval = twilio.verify_email(pre_input, code)
            elif mode == "SMS":
                twilio = TwoFA()
                rval = twilio.verify_sms(pre_input, code)
            elif mode == "APP":
                twilio = TwoFA()
                rval = twilio.verify_app(secret, code)
            if rval is True:
                # request.session["is_2fa"] = True
                return HttpResponse()
            return HttpResponseBadRequest("Failure to verify")

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")


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
            code = self.request.POST.get("code")
            user = authenticate(self.request, username=username, password=password)
            rval = verify_two_fa(user, code)
            if rval:
                auth_login(self.request, form.get_user())
                return render(self.request, "accounts/success-login.html")

            """Security check complete. Log the user in."""
        except Exception as e:
            return HttpResponseBadRequest(f"Bad Request:{e}")
        return HttpResponseBadRequest("Bad Request")

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
        # request.session["is_2fa"] = False
        return super().post(request, *args, **kwargs)


class SignupView(CreateView):

    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:success-signup")

    # cnt = "0-"
    # try:
    #    cnt = FtUser.objects.count() + "-"
    # except:
    #    cnt = "0-"
    # extra_context = {"dummy_email": cnt + randomStr(64) + "@" + randomStr(16) + ".com"}

    def form_valid(self, form):
        """
        CreateViewのメソッドをオーバーライド
        """
        try:
            if self.request.method != "POST":
                return HttpResponseBadRequest("Bad Request")
            rval = super().form_valid(form)
            login(
                self.request,
                self.object,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            return rval
        except Exception as e:
            return HttpResponseBadRequest("Bad Request:" + e)


class SignupTmpView(CreateView):

    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:two-fa")

    # cnt = "0-"
    # try:
    #    cnt = FtUser.objects.count() + "-"
    # except:
    #    cnt = "0-"
    # extra_context = {"dummy_email": cnt + randomStr(64) + "@" + randomStr(16) + ".com"}

    def form_valid(self, form):
        """
        CreateViewのメソッドをオーバーライド
        """
        print("test No.1")
        try:
            print("test No.2")
            if self.request.method != "POST":
                print("test No.3")
                return HttpResponseBadRequest("Bad Request")

            print("test No.4")
            rval = super().form_valid(form)
            print("test No.5")
            if rval.status_code >= 300 and rval.status_code < 400:
                print("test No.6")
                login(
                    self.request,
                    self.object,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                html = render_to_string("accounts/two-fa.html", {"form": form})
                print("test No.6")
                return HttpResponse(html)
            print("test No.7")
            return HttpResponseBadRequest(rval)
        except Exception as e:
            print("test No.8")
            return HttpResponseServerError("Bad Request:" + e)


def signup_valid(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # バリデーションが成功した場合、次のステップへ進む
            if form["auth"] == AuthChoices.APP:
                two_fa = TwoFA()
                (_, form["app_secret"]) = two_fa.init_app(form["email"])

            data = {"valid": True}
            return JsonResponse(data)
        else:
            html = render_to_string(
                "accounts/signup.html", {"form": form}, request=request
            )
            data = {"valid": False, "html": html}
            return JsonResponse(data)
    return HttpResponseBadRequest("Bad Request")


def SignupSuccess(request):
    context = {}
    return render(request, "accounts/success-login.html", context)


def LoginSuccess(request):
    context = {}
    return render(request, "accounts/success-login.html", context)


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
    except Exception as e:
        return HttpResponseBadRequest(f"Bad Request:{e}")


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
            if mode == "EMAIL":
                email_address = request.POST.get("id")
                code = generate_secure_random_number()
                twilio = TwoFA()
                rval = twilio.email(email_address, code)
                if rval:
                    return HttpResponse()
            elif mode == "SMS":
                phone_number = request.POST.get("id")
                twilio = TwoFA()
                rval = twilio.sms(phone_number)
                if rval:
                    return HttpResponse()
            elif mode == "APP":
                email_address = request.POST.get("id")
                twilio = TwoFA()
                (uri, secret) = twilio.init_app(email_address)
                qr = make_qr(uri)
                extra_context = {"app": True, "qr": qr, "app_url": secret}
                return JsonResponse(extra_context)

            return HttpResponseBadRequest("Bad Request")

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")


def two_fa_verify(request):
    if request.method == "POST":
        try:
            mode = request.POST.get("mode")
            pre_input = request.POST.get("id")
            code = request.POST.get("code")
            secret = request.POST.get("app_secret")
            rval = False
            if mode == "EMAIL":
                twilio = TwoFA()
                rval = twilio.verify_email(pre_input, code)
            elif mode == "SMS":
                twilio = TwoFA()
                rval = twilio.verify_sms(pre_input, code)
            elif mode == "APP":
                twilio = TwoFA()
                rval = twilio.verify_app(secret, code)
            if rval is True:
                # request.session["is_2fa"] = True
                return HttpResponse()
            return HttpResponseBadRequest("Failure to verify")

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")
