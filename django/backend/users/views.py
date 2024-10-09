from django.shortcuts import render, redirect
from django.db import models
from django.http import Http404
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, TemplateView
import hashlib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_not_required

# from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from .forms import UserEditForm
from accounts.forms import UploadAvatarForm

from django.http import (
    HttpResponseNotFound,
)


# Create your views here.
class Users(models.Model, LoginRequiredMixin):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


# def my_etag(request, *args, **kwargs):
#     return hashlib.md5(
#         ":".join(request.GET.dict().values()).encode("utf-8")
#     ).hexdigest()


# class Profile(TemplateView):
class Profile(TemplateView):
    def get(self, request):
        context = self.get_context_data()
        user = request.user
        lose_by_default = user.match_count - (user.win_count + user.loose_count)

        context["lose_by_default"] = lose_by_default
        return render(request, "users/profile.html", context)


# ユーザ情報の編集を保存する
class EditProfileView(LoginRequiredMixin, FormView):
    template_name = "users/edit-profile.html"
    form_class = UserEditForm
    # success_url = "users/profile"  # 成功時のリダイレクト先
    # success_url = "users/profile.html"  # 成功時のリダイレクト先
    success_url = reverse_lazy("users:profile")  # 成功時のリダイレクト先

    def get_form(self, *args, **kwargs):
        # request.user をフォームのインスタンスとして渡す
        return self.form_class(instance=self.request.user, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        # コンテキストに avatar フォームを追加
        context = super().get_context_data(**kwargs)
        context["avatar"] = UploadAvatarForm()
        return context

    def form_valid(self, form):
        # フォームが有効である場合にユーザー情報を保存
        form.save()
        return super().form_valid(form)


# ユーザ情報を論理削除する
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


@method_decorator(login_not_required, name="dispatch")
class PrivacyPolicy(TemplateView):
    template_name = "users/privacy-policy.html"


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
