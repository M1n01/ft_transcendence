from django import forms
from accounts.models import FtUser

from accounts.models import AuthChoices, LanguageChoice, COUNTRY_CODE_CHOICES

# from phonenumbers import COUNTRY_CODE_TO_REGION_CODE
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
import logging
import re

from django.conf import settings

USERNAME_MAX_LEN = getattr(settings, "USERNAME_MAX_LEN", None)
LASTNAME_MAX_LEN = getattr(settings, "LASTNAME_MAX_LEN", None)
FIRSTNAME_MAX_LEN = getattr(settings, "FIRSTNAME_MAX_LEN", None)
EMAIL_MAX_LEN = getattr(settings, "EMAIL_MAX_LEN", None)
PHONE_MAX_LEN = getattr(settings, "PHONE_MAX_LEN", None)
PASSWORD_MIN_LEN = getattr(settings, "PASSWORD_MIN_LEN", None)
PASSWORD_MAX_LEN = getattr(settings, "PASSWORD_MAX_LEN", None)


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        max_length=USERNAME_MAX_LEN,
        widget=forms.TextInput(
            attrs={
                "id": "username_id",
                "class": "form-control w-100 rounded-0",
                "placeholder": _("username"),
            }
        ),
    )
    email = forms.EmailField(
        # required=False,
        max_length=EMAIL_MAX_LEN,
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
        required=False,
        max_length=FIRSTNAME_MAX_LEN,
        widget=forms.TextInput(
            attrs={
                "id": "first_name_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("first_name"),
            }
        ),
    )
    last_name = forms.CharField(
        required=False,
        max_length=LASTNAME_MAX_LEN,
        widget=forms.TextInput(
            attrs={
                "id": "last_name_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("last_name"),
            }
        ),
    )
    birth_date = forms.DateField(
        required=False,
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
        max_length=PHONE_MAX_LEN,
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

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop("user_id", None)  # user.idをformに渡す
        self.auth = kwargs.pop("auth", None)  # user.authをformに渡す
        super(UserEditForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError(_("入力してください。"))
        elif len(username) > USERNAME_MAX_LEN:
            raise forms.ValidationError(_("16文字以内にしてください"))
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError(_("入力してください。"))
        #     if self.auth == AuthChoices.EMAIL:
        #         raise forms.ValidationError(
        #             _("２要素認証で必要です。メールアドレスを入力してください")
        #         )
        #     return email
        if FtUser.objects.filter(email=email).exclude(id=self.user_id).exists():
            raise forms.ValidationError(
                _("このメールアドレスは既に使用されています。......")
            )
        return email

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            last_name = None
        elif len(last_name) > LASTNAME_MAX_LEN:
            raise forms.ValidationError(_("64文字以内にしてください"))
        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            first_name = None
        elif len(first_name) > LASTNAME_MAX_LEN:
            raise forms.ValidationError(_("64文字以内にしてください"))
        return first_name

    def clean_birth_date(self):
        date = self.cleaned_data.get("birth_date")
        if not date:
            date = None
        return date

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if not phone:
            if self.auth == AuthChoices.SMS:
                raise forms.ValidationError(
                    _("２要素認証で必要です。電話番号を入力してください")
                )
            phone = None
            return phone
        pattern = "\\d*"
        result = re.fullmatch(pattern, phone)
        if result is None:
            raise forms.ValidationError(_("数値以外は記入しないでください"))

        if len(phone) > PHONE_MAX_LEN:
            raise forms.ValidationError(_("正しい電話番号を入力してください"))
        return phone


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        min_length=PASSWORD_MIN_LEN,
        max_length=PASSWORD_MAX_LEN,
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
        min_length=PASSWORD_MIN_LEN,
        max_length=PASSWORD_MAX_LEN,
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
        min_length=PASSWORD_MIN_LEN,
        max_length=PASSWORD_MAX_LEN,
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

    def clean_old_password(self):
        old_password = super().clean_old_password()
        if len(old_password) > PASSWORD_MAX_LEN:
            logging.error("Old Password  Error")
            raise forms.ValidationError(_("20文字以内にしてください"))
        if len(old_password) < PASSWORD_MIN_LEN:
            logging.error("Old Password  Error")
            raise forms.ValidationError(_("8文字以上にしてください"))
        return old_password

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        if len(new_password1) > PASSWORD_MAX_LEN:
            logging.error("New Password1  Error")
            raise forms.ValidationError(_("20文字以内にしてください"))
        if len(new_password1) < PASSWORD_MIN_LEN:
            logging.error("New Password1  Error")
            raise forms.ValidationError(_("8文字以上にしてください"))
        return new_password1

    def clean_new_password2(self):
        new_password2 = self.cleaned_data.get("new_password2")
        if len(new_password2) > PASSWORD_MAX_LEN:
            logging.error("New Password2  Error")
            raise forms.ValidationError(_("20文字以内にしてください"))
        if len(new_password2) < PASSWORD_MIN_LEN:
            logging.error("New Password2  Error")
            raise forms.ValidationError(_("8文字以上にしてください"))
        return new_password2

    # フォーム全体へのバリデーション処理を追加する場合はここ。
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
