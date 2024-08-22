from django.conf import settings
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.template.exceptions import TemplateDoesNotExist
from django.db import IntegrityError
from .models import FtTmpUser

# from django.contrib.auth.models import User

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
from .forms import SignUpForm, SignUpTmpForm
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
from .backend import TmpUserBackend


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
        rval = two_fa.verify_sms(user, code)
    elif two_fa_mode == AuthChoices.EMAIL:
        rval = two_fa.verify_email(user, code)
    elif two_fa_mode == AuthChoices.APP:
        rval = two_fa.verify_app(user, code)
    return rval


def send_two_fa_view(request):
    user = request.user
    rval = send_two_fa(user)
    if rval is False:
        return HttpResponseServerError()
    return HttpResponse()


def send_two_fa(user):
    try:
        print("send_two_fa No.1")
        two_fa_mode = user.auth
        print("send_two_fa No.2")
        two_fa = TwoFA()
        print("send_two_fa No.3")
        if two_fa_mode == AuthChoices.SMS:
            print("send_two_fa No.4")
            rval = two_fa.sms(user)
        elif two_fa_mode == AuthChoices.EMAIL:
            rval = two_fa.email(user)
        elif two_fa_mode == AuthChoices.APP:
            rval = two_fa.app(user)
        return rval
    except Exception as e:
        print(f"{e=}")
        return False


def send_two_fa_with_form(form):
    try:
        print("test fwo-fa app No.2")
        two_fa_mode = form.cleaned_data["auth"]
        email = form.cleaned_data["email"]
        print("test fwo-fa app No.3")
        user = FtUser.objects.get(email=email)
        print("test fwo-fa app No.4")
        two_fa = TwoFA()
        print("test fwo-fa app No.5")
        if two_fa_mode == AuthChoices.SMS:
            rval = two_fa.sms(user)
        elif two_fa_mode == AuthChoices.EMAIL:
            email = form.cleaned_data["email"]
            rval = two_fa.email(user)
        elif two_fa_mode == AuthChoices.APP:
            # two_fa.make_qr(user)
            print("test fwo-fa app No.6")
            rval = two_fa.app(user)
        return rval
    except Exception as e:
        print(f"{e=}")
        return False


class UserTmpLogin(LoginView):
    def form_invalid(self, form):
        return HttpResponseBadRequest("Bad Request")

    def form_valid(self, form):
        print("form_valid User Login No.1")
        """
        Login認証が成功時の戻り値をオーバーライド
        """

        """Security check complete. Log the user in."""
        try:
            print("form_valid User Login No.2")
            if self.request.method != "POST":
                print("form_valid User Login No.3")
                return HttpResponseBadRequest("Bad Request")
            print("form_valid User Login No.4")
            username = self.request.POST.get("username")
            password = self.request.POST.get("password")
            print("form_valid User Login No.5")
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                print("form_valid User Login No.6")
                return HttpResponseBadRequest("Bad Request")
            print("form_valid User Login No.7")
            rval = send_two_fa(user)
            print("form_valid User Login No.8")
            if rval:
                self.request.session["is_provisional"] = True
                print("form_valid User Login No.9")
                return HttpResponse()
        except TemplateDoesNotExist as e:
            return HttpResponseBadRequest(f"Bad Request:{e}")
        except Exception as e:
            return HttpResponseBadRequest(f"Bad Request:{e}")
        else:
            return HttpResponseBadRequest("Bad Request")


def signup_two_fa(request):
    print("signup_two_fa No.1")
    if request.method == "POST":
        print("signup_two_fa No.2")
        pass
    elif request.method == "GET":
        print("signup_two_fa No.3")
        try:
            user = request.user
            print("signup_two_fa No.4")
            two_fa_mode = user.auth
            print("signup_two_fa No.5")
            # print(f"signup_two_fa No.6 {rval=}")
            # if rval is False:
            # print("signup_two_fa No.7")
            # return HttpResponseServerError(f"Bad Request:{e}")
            if two_fa_mode == AuthChoices.SMS:
                print("signup_two_fa No.8")
                response = render(request, "accounts/signup-two-fa.html")
            elif two_fa_mode == AuthChoices.EMAIL:
                print("signup_two_fa No.9")
                response = render(request, "accounts/signup-two-fa.html")
            elif two_fa_mode == AuthChoices.APP:
                print("signup_two_fa No.10")
                rval = send_two_fa(user)
                data = {"is_auth_app": True, "qr": make_qr(rval)}
                response = render(request, "accounts/signup-two-fa.html", data)
            print(f"signup_two_fa No.11 {response.status_code=}")
            return response

        except Exception as e:
            print("signup_two_fa No.12")
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

        # new_user.email = user.email
        # new_user.email42 = user.email42
        # new_user.password = user.password
        # new_user.password = "AAdfBC3DfwFi49"
        # print(f"{new_user.password=}")
        # new_user.first_name = user.first_name
        # new_user.last_name = user.last_name
        # new_user.country_code = user.country_code
        # new_user.phone = user.phone
        # new_user.is_superuser = user.is_superuser
        # new_user.is_ft = user.is_ft
        # new_user.is_active = user.is_active
        # new_user.birth_date = user.birth_date
        # new_user.auth = user.auth
        # new_user.app_secret = user.app_secret
        # print("copy_tmpuser_to_ftuser No.1")
        # new_user.save()
        # return new_user
        print("copy_tmpuser_to_ftuser No.2")
    except IntegrityError as e:
        print(f"Copy Error:{e}")
    except Exception as e:
        print(f"Copy Error:{e}")


def signup_two_fa_verify(request):
    print("signup_two_fa_verify No.1")
    if request.method == "POST":
        print("signup_two_fa_verify No.2")
        try:
            print("signup_two_fa_verify No.3")
            user = request.user
            print("signup_two_fa_verify No.4")
            # copy_tmpuser_to_ftuser(user)
            print("signup_two_fa_verify No.5")
            code = request.POST.get("code")
            rval = verify_two_fa(user, code)
            print("signup_two_fa_verify No.6")

            if rval is False:
                print("signup_two_fa_verify No.7")
                return HttpResponseBadRequest("Failure to verify")
            print("signup_two_fa_verify No.8")
            copy_tmpuser_to_ftuser(user)

            # new_user = authenticate(
            # request, username=user.email, password=test_user.password
            # )
            # if new_user is None:
            # print("New User is None")
            # else:
            # print("New User Exist")
            print("signup_two_fa_verify No.9")
            new_user = FtUser.objects.get(email=user.email)
            # src_user = FtTmpUser.objects.get(email=user.email)
            login(
                request,
                new_user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            print("signup_two_fa_verify No.10")
            return HttpResponse()

        except json.JSONDecodeError:
            return HttpResponseServerError("Server Error")
            return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")


def two_fa_verify(request):
    if request.method == "POST":
        try:
            user = request.user
            code = request.POST.get("code")
            rval = False

            rval = verify_two_fa(user, code)

            if rval is True:
                # return HttpResponse()
                return render(request, "accounts/success-login.html")
            return HttpResponseBadRequest("Failure to verify")

        except json.JSONDecodeError:
            return HttpResponseServerError("Server Error")
            return HttpResponseBadRequest("Bad Request")
    else:
        return HttpResponseBadRequest("Bad Request")


class UserLogin(LoginView):
    ft_oauth = FtOAuth()
    # ft_oauth = TmpUserBackend()
    url = ft_oauth.get_ft_authorization_url()
    form_class = LoginFrom
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

        print("User Login No.1")
        try:
            if self.request.method != "POST":
                return HttpResponseBadRequest("Bad Request")

            print("User Login No.2")
            username = self.request.POST.get("username")
            password = self.request.POST.get("password")
            print("User Login No.3")
            code = self.request.POST.get("code")
            print("User Login No.4")
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                print("User Is None")
            print(f"User Login No.5-1 {code=}")
            print(f"User Login No.5-2 {user.auth=}")
            # rval = verify_two_fa(user, code)
            rval = send_two_fa(user)
            print("User Login No.6")
            if rval:
                print("User Login No.7")
                auth_login(self.request, form.get_user())
                is_app = user.auth == AuthChoices.APP
                print(f"User Login No.8:{is_app=}")
                data = {"is_auth_app": is_app}
                return render(self.request, "accounts/two-fa.html", context=data)

            print("User Login No.9")
            """Security check complete. Log the user in."""
        except Exception as e:
            print("User Login No.10")
            return HttpResponseBadRequest(f"Bad Request:{e}")
        print("User Login No.11")
        return HttpResponseBadRequest("Bad Request")

    def form_invalid(self, form):
        """
        Login認証が失敗時の戻り値をオーバーライド
        現在は特に変更する必要がないので、そのまま返す
        """
        print("User Login Invalid No.1")
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class UserLogout(LogoutView):
    redirect_field_name = "redirect"
    success_url = reverse_lazy("accounts:success-logout")

    def post(self, request, *args, **kwargs):
        # request.session["is_2fa"] = False
        return super().post(request, *args, **kwargs)


class SignupView(CreateView):

    form_class = SignUpTmpForm
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

    def make_two_fa_html(self, form):
        print("test fwo-fa app No.1")
        rval = send_two_fa_with_form(form)
        if rval is False:
            raise Exception

        two_fa_mode = form.cleaned_data["auth"]

        if two_fa_mode == AuthChoices.SMS:
            html = render_to_string("accounts/signup-two-fa.html")
        elif two_fa_mode == AuthChoices.EMAIL:
            html = render_to_string("accounts/signup-two-fa.html")
        elif two_fa_mode == AuthChoices.APP:
            data = {"is_auth_app": True, "qr": make_qr(rval)}
            html = render_to_string("accounts/signup-two-fa.html", data)
        return html

    def form_valid(self, form):
        """
        CreateViewのメソッドをオーバーライド
        """
        print("test No.1")
        try:
            if self.request.method != "POST":
                return HttpResponseBadRequest("Bad Request")
            rval = super().form_valid(form)
            if rval.status_code >= 300 and rval.status_code < 400:
                login(
                    self.request,
                    self.object,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                # user = form.get_user()
                # html = self.make_two_fa_html(form)
                url = "accounts/signup-two-fa.html"

                # html = render_to_string("accounts/signup-two-fa.html", {"form": form})
                # html = render_to_string("accounts/two-fa.html", {"form": form})
                return HttpResponse(url)
            print("test No.7")
            return HttpResponseBadRequest(rval)
        except Exception as e:
            print("test No.8")
            return HttpResponseServerError("Bad Request:" + e)


def signup_valid(request):
    print("signup_valid No.1")
    if request.method == "POST":
        print("signup_valid No.2")
        try:
            print("signup_valid No.3")
            form = SignUpForm(request.POST)
            print("signup_valid No.4")
            if form.is_valid():
                print("signup_valid No.5")
                # バリデーションが成功した場合、次のステップへ進む
                if form["auth"] == AuthChoices.APP:
                    two_fa = TwoFA()
                    (_, form["app_secret"]) = two_fa.init_app(form["email"])
                print("signup_valid No.6")

                tmp_form = SignUpTmpForm(request.POST)
                print("signup_valid No.6-2")

                tmp_form.save()
                print("signup_valid No.7")

                email = form.cleaned_data["email"]
                password = form.cleaned_data["password1"]
                # user = FtTmpUser.objects.get(email=email)
                print("signup_valid No.8")
                backend = TmpUserBackend()
                user = backend.authenticate(request, email=email, password=password)
                print("signup_valid No.8-2")
                if user is None:
                    print("user Is None")
                print(f"signup_valid No.9 {user=}")
                login(
                    request,
                    user,
                    backend="accounts.backend.TmpUserBackend",
                )
                print("signup_valid No.10")

                # url = "accounts/signup-two-fa.html"
                rval = send_two_fa(user)
                print("signup_valid No.11")
                if rval is False:
                    return HttpResponseServerError("Bad Request")
                two_fa_mode = user.auth
                print("signup_valid No.12")
                if two_fa_mode == AuthChoices.SMS:
                    # response = render(request, "accounts/signup-two-fa.html")
                    html = render_to_string(
                        "accounts/signup-two-fa.html", request=request
                    )
                elif two_fa_mode == AuthChoices.EMAIL:
                    html = render_to_string(
                        "accounts/signup-two-fa.html", request=request
                    )
                elif two_fa_mode == AuthChoices.APP:
                    context = {"is_auth_app": True, "qr": make_qr(rval)}
                    html = render_to_string(
                        "accounts/signup-two-fa.html", request=request, context=context
                    )
                # rval = send_two_fa_with_form(form)
                # rval = make_two_fa_html(form)
                print("signup_valid No.13")
                data = {"valid": True, "html": html}
                return JsonResponse(data)
            else:
                print("signup_valid No.14")
                html = render_to_string(
                    "accounts/signup.html", {"form": form}, request=request
                )

                data = {"valid": False, "html": html}
                return JsonResponse(data)
        except Exception as e:
            print("signup_valid No.15")
            return HttpResponseServerError(f"Server Error:{e}")
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


# def two_fa(form):
#    """
#    2認証のモードとその値を元に、認証サービスにデータを送信する
#    引数:
#        request:    ブラウザからのリクエストデータ
#    戻り値:
#        Response:   クライアントに返すレスポンスデータ
#    """
#
#    email = form.cleaned_data["email"]
#    auth = form.cleaned_data["auth"]
#    country_code = form.cleaned_data["country_code"]
#    phone = form.cleaned_data["phone"]
#    app_secret = form.cleaned_data["app_secret"]
#
#    if request.method == "GET":
#        return render(request, "accounts/two-fa.html")
#
#    if request.method == "POST":
#        try:
#            mode = request.POST.get("mode")
#            if mode == "EMAIL":
#                email_address = request.POST.get("id")
#                code = generate_secure_random_number()
#                twilio = TwoFA()
#                rval = twilio.email(email_address, code)
#                if rval:
#                    return HttpResponse()
#            elif mode == "SMS":
#                phone_number = request.POST.get("id")
#                twilio = TwoFA()
#                rval = twilio.sms(phone_number)
#                if rval:
#                    return HttpResponse()
#            elif mode == "APP":
#                email_address = request.POST.get("id")
#                twilio = TwoFA()
#                (uri, secret) = twilio.init_app(email_address)
#                qr = make_qr(uri)
#                extra_context = {"app": True, "qr": qr, "app_url": secret}
#                return JsonResponse(extra_context)
#
#            return HttpResponseBadRequest("Bad Request")
#
#        except json.JSONDecodeError:
#            return HttpResponseBadRequest("Bad Request")
#    else:
#        return HttpResponseBadRequest("Bad Request")


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
                user = FtUser.objects.get(email=email_address)
                twilio = TwoFA()
                rval = twilio.email(user)
                if rval:
                    return HttpResponse()
            elif mode == "SMS":
                # phone_number = request.POST.get("id")
                twilio = TwoFA()
                rval = twilio.sms(user)
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


# def two_fa_verify(form):
#    try:
#        mode = request.POST.get("mode")
#        pre_input = request.POST.get("id")
#        code = request.POST.get("code")
#        secret = request.POST.get("app_secret")
#        rval = False
#        if mode == "EMAIL":
#            twilio = TwoFA()
#            rval = twilio.verify_email(pre_input, code)
#        elif mode == "SMS":
#            twilio = TwoFA()
#            rval = twilio.verify_sms(pre_input, code)
#        elif mode == "APP":
#            twilio = TwoFA()
#            rval = twilio.verify_app(secret, code)
#        if rval is True:
#            # request.session["is_2fa"] = True
#            return HttpResponse()
#        return HttpResponseBadRequest("Failure to verify")
#
#    except json.JSONDecodeError:
#        return HttpResponseBadRequest("Bad Request")


# def two_fa_verify(request):
#    if request.method == "POST":
#        try:
#            mode = request.POST.get("mode")
#            pre_input = request.POST.get("id")
#            code = request.POST.get("code")
#            secret = request.POST.get("app_secret")
#            rval = False
#            if mode == "EMAIL":
#                twilio = TwoFA()
#                rval = twilio.verify_email(pre_input, code)
#            elif mode == "SMS":
#                twilio = TwoFA()
#                rval = twilio.verify_sms(pre_input, code)
#            elif mode == "APP":
#                twilio = TwoFA()
#                rval = twilio.verify_app(secret, code)
#            if rval is True:
#                # request.session["is_2fa"] = True
#                return HttpResponse()
#            return HttpResponseBadRequest("Failure to verify")
#
#        except json.JSONDecodeError:
#            return HttpResponseBadRequest("Bad Request")
#    else:
#        return HttpResponseBadRequest("Bad Request")
