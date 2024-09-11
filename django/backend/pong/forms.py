from django import forms
from .models import Tournament
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone, timedelta


class TournamentForm(forms.ModelForm):
    start_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "id": "start-datetime",
                "class": "form-control datetimepicker-input mt-5 text-black",
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
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": _("トーナメント名")}))

    class Meta:
        model = Tournament
        fields = (
            "name",
            "is_only_friend",
            "current_players",
            "start_at",
        )
