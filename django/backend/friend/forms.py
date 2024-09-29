from django import forms
from .models import Friendships

from django.utils.translation import gettext_lazy as _


class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = Friendships
        fields = ("friend",)


class SearchFriendForm(forms.Form):
    # query = forms.CharField(label=_(""), max_length=100, placeholder=_("ユーザー名"))
    query = forms.CharField(
        max_length=32,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control  rounded-0 ",
                "type": "search",
                "placeholder": _("ユーザー名"),
            }
        ),
    )

    # class Meta:
    # model = Friendships
    # fields = "friend"
