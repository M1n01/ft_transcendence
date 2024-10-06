from django.db import models
from accounts.models import FtUser

# Create your models here.


class UserActionLog(models.Model):
    user = models.ForeignKey(FtUser, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=256, unique=False)
    method = models.CharField(max_length=16, unique=False)
    status_code = models.IntegerField(null=True, blank=True)
