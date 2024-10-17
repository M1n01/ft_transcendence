from django import forms
from accounts.models import FtUser

from accounts.models import LanguageChoice, COUNTRY_CODE_CHOICES

# from phonenumbers import COUNTRY_CODE_TO_REGION_CODE
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

# import re


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "username_id",
                "class": "form-control w-100 rounded-0",
                "placeholder": _("username"),
            }
        ),
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "email_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "type": "email",
                "placeholder": _("username"),
            }
        ),
    )
    first_name = forms.CharField(
        # required=False,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "id": "first_name_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("first_name"),
            }
        ),
    )
    last_name = forms.CharField(
        # required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "id": "last_name_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("last_name"),
            }
        ),
    )
    birth_date = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "birth_date_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("birth_date"),
                "type": "date",
            }
        ),
    )
    country_code = forms.ChoiceField(
        choices=COUNTRY_CODE_CHOICES,
        initial="+81",
        widget=forms.Select(
            attrs={
                "id": "country_code_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("country_code"),
            }
        ),
    )
    phone = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "id": "phone_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("phone_number"),
            },
        ),
    )
    language = forms.ChoiceField(
        choices=LanguageChoice,
        initial=LanguageChoice.JP,
        widget=forms.Select(
            attrs={
                "id": "language_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("language"),
            }
        ),
    )

    class Meta:
        model = FtUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "country_code",
            "phone",
            "language",
        )


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "id": "old_password_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("現在のパスワード"),
                "autocomplete": "old_password",
                "aria-labelledby": "passwordHelpBlock",
            }
        ),
    )
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "id": "new_password_id1",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("新しいパスワード"),
                "autocomplete": "new_password1",
                "aria-labelledby": "passwordHelpBlock",
            }
        ),
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "id": "new_password_id2",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("新しいパスワード(確認用)"),
                "autocomplete": "new_password2",
                "aria-labelledby": "passwordHelpBlock",
            }
        ),
    )

    class Meta:
        model = FtUser
        fields = ["old_password", "new_password1", "new_password2"]

    # バリデーション処理を追加する場合はここ。
    def clean(self):
        # デフォルトバリデーションを実行
        cleaned_data = super().clean()

        # old_password と new_password1 が同じかチェック
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        if old_password and new_password1 and old_password == new_password1:
            self.add_error(
                "new_password1",
                _("新しいパスワードは古いパスワードと同じにできません。"),
            )
        # TODO: debug用。あとで消す。
        # print("ValidationError: ", self.errors)  # ここでエラーを出力

        return cleaned_data
