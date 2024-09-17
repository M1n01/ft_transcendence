from django import forms
from .models import Tournament
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone, timedelta


class TournamentForm(forms.ModelForm):
    start_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "id": "start-datetime",
                "class": "form-control datetimepicker-input text-black",
                "verbose_name": _("最大参加人数"),
                "placeholder": _("トーナメント開始日時"),
                "type": "datetime-local",
                "value": (
                    datetime.now(tz=timezone.utc) + timedelta(seconds=14400)
                ).strftime("%Y-%m-%dT%H:00"),
                "step": "300",
            }
        ),
    )
    name = forms.CharField(
        max_length=32,
        widget=forms.TextInput(
            attrs={
                # "placeholder": _("トーナメント名"),
                "class": "form-control w-100 ",
            }
        ),
    )
    current_players = forms.IntegerField(
        min_value=4,
        max_value=32,
        widget=forms.NumberInput(
            # attrs={
            # "placeholder": _("最大参加人数"),
            # "class": "form-control w-100 ",
            # }
        ),
    )

    organizer = forms.IntegerField(widget=forms.HiddenInput())
    is_only_friend = forms.BooleanField(
        label=_("フレンドのみ2"),
        required=False,
        widget=forms.CheckboxInput(attrs={"class": " ms-1"}),
    )

    class Meta:
        model = Tournament
        fields = (
            "name",
            "is_only_friend",
            "current_players",
            "start_at",
        )

    def set_organizer(self, name):
        self.fields["organizer"].initial = name

    def set_only_user(self, flag_str):
        if flag_str == "on":
            self.fields["is_only_friend"] = True
        elif flag_str == "off":
            self.fields["is_only_friend"] = False
        else:
            self.fields["is_only_friend"] = False
            # raise forms.ValidationError("on/off以外の文字列は仕様できません")

    # def __init__(self, *args, **kwargs):
    # super().__init__(*args, **kwargs)
    # self.fields["organizer"].initial = self.request.user
