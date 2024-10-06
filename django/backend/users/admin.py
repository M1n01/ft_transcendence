from django.contrib import admin

# Register your models here.
from .models import UserActionLog


@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ["user", "timestamp", "method", "url", "status_code"]
    search_fields = ["user__username", "method", "url", "status_code"]
