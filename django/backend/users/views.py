from django.shortcuts import render, redirect
from django.db import models
from django.http import Http404
from django.views.generic import UpdateView
import hashlib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required  # 認証が必要なページにする
from django.contrib.auth.decorators import login_not_required

# from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from .forms import UserEditForm
from accounts.forms import UploadAvatarForm

from django.http import (
    HttpResponseNotFound,
)

# loginしない限り見れない
# class Pong(LoginRequiredMixin, ListView):
# model = "test"


def checkSPA(request):
    headers = request.headers
    print(f"checkSPA:{headers=}")
    cokkie = headers.get("Cookie", "No Cookie Header Found")
    print(f"checkSPA:{cokkie=}")
    spa = request.META.get("HTTP_SPA")
    spas = request.META.get("HTTPS_SPA")
    if spa is None and spas is None:
        Http404("not allowed")
    if spa and spa == "spa":
        return True
    if spas and spas == "spa":
        return True
    Http404("not allowed")
    return False


# Create your views here.
class Users(models.Model, LoginRequiredMixin):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


def my_etag(request, *args, **kwargs):
    return hashlib.md5(
        ":".join(request.GET.dict().values()).encode("utf-8")
    ).hexdigest()


# テスト用　後で消す
# @condition(etag_func=my_etag)
def test(request):
    return render(request, "users/test.html")


def profile_view(request):
    headers = request.headers
    print(f"checkSPA:{headers=}")
    cokkie = headers.get("Cookie", "No Cookie Header Found")
    print(f"checkSPA:{cokkie=}")
    checkSPA(request)
    return render(request, "users/profile.html")


# @condition(etag_func=my_etag)
def profile(request):
    # profile_view(request)
    return render(request, "users/profile.html")


# ユーザ情報の編集を保存する
@login_required
def edit_profile(request):
    user = request.user  # ログインユーザーを取得
    avatar_class = UploadAvatarForm
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("/profile")  # 編集後、プロファイルページにリダイレクト
    else:
        form = UserEditForm(instance=user)  # フォームにユーザー情報をプリセット
    return render(
        request, "users/edit-profile.html", {"form": form, "avatar": avatar_class}
    )


# ユーザ情報を論理削除する
@login_required
def delete_user(request):
    if request.method == "POST":
        # ユーザー情報を取得
        print(f"Delete user (logical): {request.user}")

        # ユーザーの論理削除 (is_activeをFalseに設定)
        # request.user.username = ""
        # request.user.email = None
        # request.user.email42 = None
        request.user.email = str(request.user.id) + "user@tmp.email.com"
        request.user.email42 = str(request.user.id) + "user@tmp.email.com"
        request.user.first_name = None
        request.user.last_name = None
        request.user.country_code = None
        request.user.phone = None
        request.user.language = ""
        request.user.is_active = False
        # request.user.is_temporary = False
        request.user.birth_date = None
        request.user.auth = ""
        request.user.app_secret = None
        request.user.created_at = None
        request.user.updated_at = None

        request.user.save()
        # request.user.logout()

        # print(request.user)
        # 適切なリダイレクト先に遷移
        return redirect("/")

    return render(request, "users/delete-user.html")


# TODO: あとで削除
def cookie_banner(request):
    return render(request, "users/cookie-banner.html")


@login_not_required
def privacy_policy(request):
    return render(request, "users/privacy-policy.html")


class UpdateAvatar(UpdateView):
    form_class = UploadAvatarForm
    template_name = "user/profile.html"  # 使わない
    success_url = reverse_lazy("friend:friend")  # 使わない

    def get(self, request):
        """
        GETは禁止
        """
        return HttpResponseNotFound()

    def get_object(self):
        return self.request.user
