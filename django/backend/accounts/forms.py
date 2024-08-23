from django.contrib.auth.forms import UserCreationForm
from django import forms

# from .modelss import User, FtUser
from .models import FtUser
from .models import FtTmpUser

# from .models import LanguageChoice


class SignUpForm(UserCreationForm):
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
