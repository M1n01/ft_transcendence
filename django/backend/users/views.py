import csv
from django.shortcuts import render
from django.db import models
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, TemplateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .forms import UserEditForm, ChangePasswordForm
from accounts.forms import UploadAvatarForm

from accounts.models import FtUser

from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)


# Create your views here.
class Users(models.Model, LoginRequiredMixin):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


# プロフィール画面の表示
class ProfileView(TemplateView):
    def get(self, request):
        context = self.get_context_data()
        user = request.user
        lose_by_default = user.match_count - (user.win_count + user.loose_count)

        context["lose_by_default"] = lose_by_default
        return render(request, "users/profile.html", context)


# ユーザ情報の編集を保存する
class EditProfileView(LoginRequiredMixin, FormView):
    form_class = UserEditForm
    template_name = "users/edit-profile.html"
    success_url = "/users/profile"  # 使わない

    def get_form(self, *args, **kwargs):
        # request.user をフォームのインスタンスとして渡す
        return self.form_class(instance=self.request.user, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        # コンテキストに avatar フォームを追加
        context = super().get_context_data(**kwargs)
        context["avatar"] = UploadAvatarForm()
        return context

    def form_valid(self, form):
        try:
            # フォームが有効である場合にユーザー情報を保存
            form.save()
            response = super().form_valid(form)
            response.status_code = 200
            return response
        except Exception as e:
            return HttpResponseBadRequest(f"Bad Request:{e}")


# パスワードの変更
class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = "users/change-password.html"
    success_url = reverse_lazy("users:changed-password")  # 使わない

    def form_invalid(self, form):
        # TODO: debug用。あとで消す
        # print("ValidationError:", form.errors)  # ここでエラーを出力
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class ChangedPasswordView(TemplateView):
    def get(self, request):
        context = self.get_context_data()

        return render(request, "users/changed-password.html", context)


class ExportProfileView(LoginRequiredMixin, View):
    # 認証されていないユーザーがアクセスしようとした場合のリダイレクトURL
    login_url = "/"

    def get(self, request, *args, **kwargs):
        # HTTPレスポンスをCSV形式で作成
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="profile_data.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "Username",
                "Email",
                "first_name",
                "last_name",
                "birth_date",
                "country_code",
                "phone",
                "language",
                "created_at",
                "updated_at",
                "last_login",
            ]
        )  # ヘッダー行の作成

        # ユーザーデータを取得し、CSVに書き込む
        for user in FtUser.objects.all():
            writer.writerow(
                [
                    user.username,
                    user.email,
                    user.first_name,
                    user.last_name,
                    user.birth_date,
                    user.country_code,
                    user.phone,
                    user.language,
                    user.created_at,
                    user.updated_at,
                    user.last_login,
                ]
            )

        print(response)
        return response


class ExportedProfileView(TemplateView):
    def get(self, request):
        context = self.get_context_data()

        return render(request, "users/exported-profile.html", context)


# ユーザ情報を論理削除する
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = FtUser
    success_url = "/"  # 使わない

    def post(self, request, *args, **kwargs):
        try:
            user = self.get_object()  # 削除対象のユーザーオブジェクトを取得
            # user = request.user  # 削除対象のユーザーオブジェクトを取得

            # ユーザーの論理削除 (is_activeをFalseに設定)
            user.username = "delete_user_" + str(user.id)
            # request.user.email = None
            # request.user.email42 = None
            temp_email = str(user.id) + "user@tmp.email.com"
            user.email = temp_email
            user.email42 = temp_email
            user.first_name = None
            user.last_name = None
            user.country_code = None
            user.phone = None
            user.language = ""
            user.is_active = False
            user.birth_date = None
            user.auth = ""
            user.app_secret = None
            # user.created_at = None
            # user.updated_at = None

            user.save()
            print("Execute DeleteUserView")
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            print(f"Error deleting user: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    def get(self):
        """
        GETは禁止
        """
        return HttpResponseNotFound()

    def get_object(self):
        return self.request.user


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
