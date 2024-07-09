from django.contrib import admin

# from .modelss import User
from .models.user import User

# Register your models here.

admin.site.register(User)
