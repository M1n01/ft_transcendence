from django.db import models
from django.utils import timezone
import datetime

from accounts.models import FtUser


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class GAME_CHOICES(models.TextChoices):
    PONG1 = "PO1", "PONG1"
    PONG2 = "PO2", "PONG2"


class Game(models.Model):
    id = models.BigAutoField(primary_key=True)
    game = models.CharField(
        max_length=16,
        choices=GAME_CHOICES,
        default=GAME_CHOICES.PONG1,
    )
    win_user = models.ForeignKey(
        FtUser, related_name="game_win_user", on_delete=models.CASCADE
    )
    # win_user2 = models.ForeignKey(
    # User, related_name="game_pong", on_delete=models.CASCADE, null=True
    # )
    loose_user = models.ForeignKey(
        FtUser, related_name="game_loose_user", on_delete=models.CASCADE
    )
    # loose_user2 = models.ForeignKey(
    # User, related_name="game_pong", on_delete=models.CASCADE, null=True
    # )
    win_score = models.SmallIntegerField()
    lose_score = models.SmallIntegerField()

    def __str__(self):
        return f"id={self.id}: {self.game}"
