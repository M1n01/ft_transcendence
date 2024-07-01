from django.contrib import admin
from django.contrib.auth.models import Group
import os

from .models import User

# Register your models here.

# admin.site.register(User)
admin.site.register(User)
admin.site.unregister(Group)


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ft_trans.settings")
