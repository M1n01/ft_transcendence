from django import forms
from .models import Tournament, TournamentParticipant
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone


TIME_HOUR_CHOICES = [((f"{hour:02d}"), f"{hour:02d}") for hour in range(0, 24)]
TIME_MINUTE_CHOICES = [
    ((f"{minute:02d}"), f"{minute:02d}") for minute in [0, 15, 30, 45]
]


class TournamentParticipantForm(forms.ModelForm):
    # is_accept = forms.BooleanField()
    # participant = forms.CharField()

    class Meta:
        model = TournamentParticipant
        fields = ("alias_name", "tournament_id")


class TournamentForm(forms.ModelForm):
    start_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "id": "start-datetime",
                "class": "form-control datetimepicker-input text-black",
                "verbose_name": _("最大参加人数"),
                "placeholder": _("トーナメント開始日"),
                "type": "date",
                "value": (
                    # datetime.now(tz=timezone.utc) + timedelta(seconds=14400)
                    datetime.now(tz=timezone.utc)
                ).strftime("%Y-%m-%d"),
                # ).strftime("%Y-%m-%dT%H:00"),
            }
        ),
    )
    # start_time = forms.ChoiceField(
    #    choices=TIME_CHOICES,
    # )

    start_hour = forms.ChoiceField(
        choices=TIME_HOUR_CHOICES,
        widget=forms.Select(attrs={"class": "dropdown-toggle  btn border text-black"}),
    )
    start_minute = forms.ChoiceField(
        choices=TIME_MINUTE_CHOICES,
        widget=forms.Select(attrs={"class": "dropdown-toggle btn border text-black"}),
    )
    # start_hour = forms.IntegerField(
    #    min_value=0,
    #    max_value=23,
    # )
    # start_minute = forms.IntegerField(
    #    min_value=0,
    #    max_value=45,
    #    step_size=15,
    # )

    name = forms.CharField(
        max_length=20,
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
        label=_("フレンドに通知"),
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
            "start_hour",
            "start_minute",
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
