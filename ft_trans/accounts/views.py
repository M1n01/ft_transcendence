from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.conf import settings
from .forms import SignUpForm
from .models import User

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
        model = User


class UserLogin(LoginView):
    # template_name = "user_login.html"
    # next_page = LOGIN_REDIRECT_URL
    # redirect_field_name = "/script"
    # authentication_form = AuthenticationForm
    # extra_context
    form_class = LoginFrom
    template_name = "accounts/login.html"
    success_url = reverse_lazy("accounts:success-login")
    # redirect_authenticated_user = False


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
    model = User
    template_name = "accounts/user_list.html"
    redirect_field_name = "redirect"


# Create your views here.
def SignupSuccess(request):
    return render(request, "accounts/success-signup.html")


def LoginSuccess(request):
    return render(request, "accounts/success-login.html")


def LogoutSuccess(request):
    return render(request, "accounts/success-logout.html")


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


# Create your views here.
