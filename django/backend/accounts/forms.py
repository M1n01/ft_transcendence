from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms

# from .modelss import User, FtUser
from .models import FtUser
from .models import FtTmpUser, AuthChoices, LanguageChoice, COUNTRY_CODE_CHOICES

# from phonenumbers import COUNTRY_CODE_TO_REGION_CODE
from django.utils.translation import gettext_lazy as _


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
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("password"),
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
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0",
                "placeholder": _("username"),
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "type": "email",
                "placeholder": _("username"),
            }
        ),
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("first_name"),
            }
        ),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("last_name"),
            }
        ),
    )

    birth_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("birth_date"),
            }
        ),
    )
    country_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("country_code"),
            }
        ),
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("phone_number"),
            }
        ),
    )
    auth = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("auth"),
            }
        ),
    )
    language = forms.MultipleChoiceField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("language"),
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("password"),
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
            "auth",
            "app_secret",
            "language",
        )
        widgets = {
            "app_secret": forms.HiddenInput(),
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }

        def clean_username(self):
            username = self.cleaned_data.get("username")
            if FtTmpUser.objects.filter(username=username).exists():
                print(f"username Error:{username=}")
                raise forms.ValidationError("このユーザー名は既に使用されています。")
            return username

        def clean_email(self):
            email = self.cleaned_data.get("email")
            if FtTmpUser.objects.filter(email=email).exists():
                print(f"email Error:{email=}")
                raise forms.ValidationError("このメールアドレスは既に使用されています。......")
            return email

        def clean_phone(self):
            phone = self.cleaned_data.get("phone")
            if FtTmpUser.objects.filter(phone=phone).exists():
                print(f"phne Error:{phone=}")
                raise forms.ValidationError("この電話番号は既に使用されています。")
            return phone


class SignUpTmpForm(UserCreationForm):
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
        widget=forms.TextInput(
            attrs={
                "id": "first_name_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("first_name"),
            }
        ),
    )
    last_name = forms.CharField(
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
        widget=forms.TextInput(
            attrs={
                "id": "phone_id",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("phone_number"),
            }
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
        widget=forms.PasswordInput(
            attrs={
                "id": "password_id1",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("password"),
            }
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "password_id2",
                "class": "form-control w-100 rounded-0 border-top-0",
                "placeholder": _("password(確認用)"),
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
            if FtTmpUser.objects.filter(username=username).exists():
                print(f"username Error:{username=}")
                raise forms.ValidationError("このユーザー名は既に使用されています。")
            return username

        def clean_email(self):
            email = self.cleaned_data.get("email")
            if FtTmpUser.objects.filter(email=email).exists():
                print(f"email Error:{email=}")
                raise forms.ValidationError("このメールアドレスは既に使用されています。......")
            return email

        def clean_phone(self):
            phone = self.cleaned_data.get("phone")
            if FtTmpUser.objects.filter(phone=phone).exists():
                print(f"phne Error:{phone=}")
                raise forms.ValidationError("この電話番号は既に使用されています。")
            return phone


class FtLoginForm(UserCreationForm):
    class Meta:
        model = FtUser
        fields = (
            "username",
            "email42",
        )
        username = forms.CharField(
            # max_length=100,
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
