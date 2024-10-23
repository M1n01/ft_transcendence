from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms

# from .modelss import User, FtUser
from .models import FtUser
from .models import FtTmpUser, AuthChoices, LanguageChoice, COUNTRY_CODE_CHOICES

# from phonenumbers import COUNTRY_CODE_TO_REGION_CODE
from django.utils.translation import gettext_lazy as _
import re
import logging

from django.conf import settings

USERNAME_MAX_LEN = getattr(settings, "USERNAME_MAX_LEN", None)
LASTNAME_MAX_LEN = getattr(settings, "LASTNAME_MAX_LEN", None)
FIRSTNAME_MAX_LEN = getattr(settings, "FIRSTNAME_MAX_LEN", None)
EMAIL_MAX_LEN = getattr(settings, "EMAIL_MAX_LEN", None)
PHONE_MAX_LEN = getattr(settings, "PHONE_MAX_LEN", None)
PASSWORD_MIN_LEN = getattr(settings, "PASSWORD_MIN_LEN", None)
PASSWORD_MAX_LEN = getattr(settings, "PASSWORD_MAX_LEN", None)

# COUNTRY_CODE_CHOICES = [
#    (f"+{code}", f"+{code} ({region[0]})")
#    for code, region in COUNTRY_CODE_TO_REGION_CODE.items()
# ]


# from .models import LanguageChoice
class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0",
                "type": "email",
                "placeholder": _("email"),
                "autocomplete": "email",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("password"),
                "aria-labelledby": "passwordHelpBlock",
                "autocomplete": "current-password",
            }
        ),
    )

    class Meta:
        model = FtUser
        fields = (
            "username",
            "email42",
        )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=USERNAME_MAX_LEN,
        widget=forms.TextInput(
            attrs={
                "id": "username_id",
                "class": "form-control w-100 rounded-0",
                "placeholder": _("username"),
                "autocomplete": "username",
            },
        ),
    )
    email = forms.CharField(
        max_length=EMAIL_MAX_LEN,
        widget=forms.TextInput(
            attrs={
                "id": "email_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "type": "email",
                "placeholder": _("username"),
                "autocomplete": "email",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=FIRSTNAME_MAX_LEN,
        widget=forms.TextInput(
            attrs={
                "id": "first_name_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("first_name"),
                "autocomplete": "first_name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=LASTNAME_MAX_LEN,
        widget=forms.TextInput(
            attrs={
                "id": "last_name_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("last_name"),
                "autocomplete": "last_name",
            }
        ),
    )
    birth_date = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "birth_date_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("birth_date"),
                "autocomplete": "birth_date",
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
                "autocomplete": "phone",
            },
        ),
    )
    auth = forms.ChoiceField(
        choices=AuthChoices,
        initial=AuthChoices.APP,
        widget=forms.Select(
            attrs={
                "id": "auth_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("auth"),
            }
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
    password1 = forms.CharField(
        min_length=PASSWORD_MIN_LEN,
        max_length=PASSWORD_MAX_LEN,
        widget=forms.PasswordInput(
            attrs={
                "id": "password_id1",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("password"),
                "aria-labelledby": "passwordHelpBlock",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        min_length=PASSWORD_MIN_LEN,
        max_length=PASSWORD_MAX_LEN,
        widget=forms.PasswordInput(
            attrs={
                "id": "password_id2",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("password(確認用)"),
                "aria-labelledby": "passwordHelpBlock",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = FtTmpUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "country_code",
            "phone",
            "auth",
            "app_secret",
            "language",
        )
        widgets = {
            "app_secret": forms.HiddenInput(),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # if FtUser.objects.filter(username=username).exists():
        # print(f"username Error:{username=}")
        # raise forms.ValidationError("このユーザー名は既に使用されています。")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if FtTmpUser.objects.filter(email=email).exists():
            print(f"email Error:{email=}")
            raise forms.ValidationError(_("このメールアドレスは既に使用されています。......"))
        if FtUser.objects.filter(email=email).exists():
            print(f"email Error:{email=}")
            raise forms.ValidationError(_("このメールアドレスは既に使用されています。......"))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        pattern = "\\d*"
        result = re.fullmatch(pattern, phone)
        if result is None:
            raise forms.ValidationError(_("数値以外は記入しないでください"))

        if len(phone) > PHONE_MAX_LEN:
            raise forms.ValidationError(_("正しい電話番号を入力してください"))

        if FtTmpUser.objects.filter(phone=phone).exists():
            print(f"email Error:{phone=}")
            raise forms.ValidationError(_("この電話番号は既に使用されています。......"))
        if FtUser.objects.filter(phone=phone).exists():
            print(f"email Error:{phone=}")
            raise forms.ValidationError(_("この電話番号は既に使用されています。......"))

        return phone

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if len(last_name) > LASTNAME_MAX_LEN:
            logging.error(f"Last Name Error:{last_name=}")
            raise forms.ValidationError(_("64文字以内にしてください"))
        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if len(first_name) > LASTNAME_MAX_LEN:
            logging.error(f"First Name Error:{first_name=}")
            raise forms.ValidationError(_("64文字以内にしてください"))
        return first_name

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) > PASSWORD_MAX_LEN:
            logging.error("Password  Error")
            raise forms.ValidationError(_("20文字以内にしてください"))
        if len(password1) < PASSWORD_MIN_LEN:
            logging.error("Password  Error")
            raise forms.ValidationError(_("8文字以上にしてください"))
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        if len(password2) > PASSWORD_MAX_LEN:
            logging.error("Password  Error")
            raise forms.ValidationError(_("20文字以内にしてください"))
        if len(password2) < PASSWORD_MIN_LEN:
            logging.error("Password  Error")
            raise forms.ValidationError(_("8文字以上にしてください"))
        return password2


class FtLoginForm(UserCreationForm):
    class Meta:
        model = FtUser
        fields = (
            "username",
            "email42",
        )
        username = forms.CharField(
            max_length=USERNAME_MAX_LEN,
            # label="ユーザー名",  # ここでラベルを指定
            widget=forms.TextInput(attrs={"class": "form-control"}),
        )
        email42 = forms.CharField(
            # max_length=100,
            # label="パスワード",  # ここでラベルを指定
            widget=forms.PasswordInput(attrs={"class": "form-control"}),
        )
        # widgets = {
        # "username": forms.TextInput(attrs={"class": "form-control"}),
        # }


class UploadAvatarForm(forms.ModelForm):
    class Meta:
        model = FtUser
        fields = ("avatar",)
        # avatar = forms.ImageField(
        #    widget=forms.URLInput(attrs={"class": "form-control btn btn-primary"}),
        # )
