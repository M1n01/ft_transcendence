from django.contrib import admin
from .models import Question
from .models import Choice

# from .models import UserName
# from .models import Email

from .models import Game

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
# admin.site.register(UserName)
# admin.site.register(Email)
admin.site.register(Game)
