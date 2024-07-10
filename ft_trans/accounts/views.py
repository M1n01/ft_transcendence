from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json


# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.conf import settings
from .forms import SignUpForm
from .forms import FtSignUpForm

# from .models import User, FtUser
from accounts.models import User
from accounts.models import FtUser
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64
from .oauth import FtOAuth

import logging


def LoginPage(request):
    return render(request, "accounts/login.html")


def LogoutPage(request):
    return render(request, "accounts/logout.html")


# class Account(CreateView):
# if self.request.user.is_authenticated:
# template_name = 'forum/register.html'
# else:
# template_name = 'forum/register.html'


class LoginFrom(AuthenticationForm):
    class Meta:
        model = FtUser


class UserLogin(LoginView):
    ft_oauth = FtOAuth()
    form_class = LoginFrom
    template_name = "accounts/login.html"
    success_url = reverse_lazy("accounts:success-login")

    # QRコード作成
    url = ft_oauth.get_ft_authorization_url()
    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer)
    qr = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    extra_context = {"qr": qr, "ft_url": url}


class UserLogout(LogoutView):
    # next_page = getattr(settings, "LOGOUT_REDIRECT_URL", None)
    # template_name = "user_logout.html"
    redirect_field_name = "redirect"
    success_url = reverse_lazy("accounts:success-logout")


class SignupView(CreateView):
    """ユーザー登録用ビュー"""

    form_class = SignUpForm  # 作成した登録用フォームを設定
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:success-signup")

    # success_url = reverse_lazy("accounts:list")
    # success_url = reverse_lazy("spa:/")  # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        print(f"from_valid () start print")
        logging.info(f"from_valid () start")
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        # account_id = form.cleaned_data.get("account_id")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        logging.info(f"from_valid username={username}, password={password}")
        user = authenticate(username=username, password=password)
        # user = authenticate(account_id=account_id, password=password)
        login(self.request, user)
        return response


"""
class UserRegistration(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        print(f"from_valid () start print No.2")
        logging.info(f"from_valid () start No.2")
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response
"""


class UserList(LoginRequiredMixin, ListView):
    model = FtUser
    template_name = "accounts/user_list.html"
    redirect_field_name = "redirect"


# Create your views here.
def SignupSuccess(request):
    return render(request, "accounts/success-signup.html")


def LoginSuccess(request):
    return render(request, "accounts/success-login.html")


def LogoutSuccess(request):
    return render(request, "accounts/success-logout.html")


def OAuthTest(request):
    return render(request, "accounts/oauth.html")


def signup_view(request):
    pass


def login_view(request):
    pass


def logout_view(request):
    pass


def user_view(request):
    pass


def other_view(request):
    pass


import asyncio


class FtLoginFrom(AuthenticationForm):
    class Meta:
        model = FtUser


# class FtUserLogin(LoginView):
## ft_oauth = FtOAuth()
# form_class = FtLoginFrom
## template_name = "accounts/login.html"
# success_url = reverse_lazy("accounts:success-login")


def oauth_login(request):
    print("form_valid test No.1")
    # if request.method == "POST":
    ft_oauth = FtOAuth()

    print("form_valid test No.2")
    # print(f"debug No.1 request.body={request.body}")
    body = json.loads(request.body)
    # print(f"debug No.2 request.body={body}")
    url = body["url"]
    # url = form.cleaned_data.get("url")
    print("form_valid test No.3")
    print(f"debug No.3 {url=}")
    token_response = ft_oauth.send_ft_authorization(url)
    # print("form_valid test No.4" + token_response)
    token_json = token_response.json()
    print("form_valid test No.4.1")

    access_token = token_json["access_token"]
    user_response = ft_oauth.fetch_user(access_token)
    print("form_valid test No.5.1")
    username = user_response["login"]
    print("form_valid test No.6.1")
    # user_json = user_response.json()
    print("form_valid test No.7.1")
    # username = user_json["username"]
    email = user_response["email"]
    print("form_valid test No.5")
    # login(self.request, username)
    print("form_valid test No.6")

    # form["username"] = username
    # form["email"] = email
    print("form_valid test No.7")
    # response_form = super().form_valid(form)
    print("form_valid test No.8")
    user = authenticate(request, username=username, email=email)
    print("form_valid test No.9")
    # user = ft_oauth.authenticate(request, username)
    if user is None:
        print("form_valid test No.10")
        user = FtUser()
        user.username = username
        user.email = email
        user.save()
        user = authenticate(request, username=username)

    if user is None:
        print("Error Error Error Error Error User is None")
    print("form_valid test No.11 username=" + username)
    login(request, user, backend="accounts.oauth.FtOAuth")
    #login(request, user, backend="django.contrib.auth.backends.RemoteUserBackend")

    # login(request, user, backend="django.contrib.auth.backends.RemoteUserBackend")
    print("form_valid test No.12")
    # else:
    # print("form_valid test No.9")
    # self.login(request, user)
    response_data = {"body": "Error: GetMethod"}
    res = JsonResponse(response_data)
    return res

    # try:
    #    user = FtUser.objects.get(username=username)
    # except FtUser.DoesNotExist:
    #    print("Error")
    #    response_data = {"body": "Error: GetMethod"}
    #    return JsonResponse(response_data)

    # login(request, user)
    print("form_valid test No.10")
    # FtUserLogin().as_view()
    # return FtUserLogin().as_view()
    # else:
    # response_data = {"body": "Error: GetMethod"}
    return user_response


class FtLoginFrom(AuthenticationForm):
    class Meta:
        model = FtUser


# class FtUserLogin(CreateView):
class FtUserLogin(LoginView):
    form_class = FtLoginFrom
    template_name = "accounts/ft-login.html"
    success_url = reverse_lazy("accounts:success-login")

    # def form_valid(self, form):
    # def login(self):
    #    print("form_valid test No.1")
    #    # if request.method == "POST":
    #    ft_oauth = FtOAuth()

    #    print("form_valid test No.2")
    #    # print(f"debug No.1 request.body={request.body}")
    #    body = json.loads(self.request.body)
    #    # print(f"debug No.2 request.body={body}")
    #    url = body["url"]
    #    # url = form.cleaned_data.get("url")
    #    print("form_valid test No.3")
    #    print(f"debug No.3 {url=}")
    #    response = ft_oauth.send_ft_authorization(url)
    #    print("form_valid test No.4")
    #    username = response.json()["login"]
    #    email = response.json()["email"]
    #    print("form_valid test No.5")
    #    # login(self.request, username)
    #    print("form_valid test No.6")

    #    # form["username"] = username
    #    # form["email"] = email
    #    print("form_valid test No.7")
    #    # response_form = super().form_valid(form)
    #    print("form_valid test No.8")
    #    user = ft_oauth.authenticate(username=username)
    #    print("form_valid test No.9")

    #    # try:
    #    #    user = FtUser.objects.get(username=username)
    #    # except FtUser.DoesNotExist:
    #    #    print("Error")
    #    #    response_data = {"body": "Error: GetMethod"}
    #    #    return JsonResponse(response_data)

    #    login(self.request, user)
    #    print("form_valid test No.10")
    #    # FtUserLogin().as_view()
    #    # return FtUserLogin().as_view()
    #    # else:
    #    # response_data = {"body": "Error: GetMethod"}
    #    return response


def redirect_oauth(request):
    print("redirect_oauth No.1")
    code = request.GET.get("code")
    state = request.GET.get("state")
    ft_oauth = FtOAuth()
    print(f"{code=}")
    print(f"{state=}")
    ft_oauth.append_state_code_dict(state, code)
    # ft_oauth.make_user(state, code)

    """
    token_response = ft_oauth.fetch_access_token(state, code)
    access_token = token_response.json()["access_token"]
    user_response = ft_oauth.fetch_user(access_token)
    result_json = user_response.json()
    username = result_json["login"]
    email = result_json["email"]
    image = result_json["image"]["link"]

    try:
        user = FtUser.objects.get(username=username)
    except FtUser.DoesNotExist:
        # DB上に存在しなければここで作成する
        new_user = FtUser()
        new_user.username = username
        new_user.email = email
        new_user.save()
    """

    return render(request, "accounts/redirect-oauth.html")


# Create your views here.
