from django import forms
from .models import Friendships

# from django.utils.translation import gettext_lazy as _


class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = Friendships
        fields = ("friend",)


class SearchFriendForm(forms.Form):
    query = forms.CharField(label="Search for a user", max_length=100)

    # class Meta:
    # model = Friendships
    # fields = "friend"
