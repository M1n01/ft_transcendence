from django.shortcuts import render
from django.views.generic import ListView
from django.utils.translation import get_language
from .models import UserNotification


# Create your views here.
class Notification(ListView):
    model = UserNotification
    template_name = "notification/notification.html"
    # context_object_name = "users"
    paginate_by = 20  # ページネーションが必要な場合

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset

    def get(self, request):
        notifications = self.model.objects.filter(user=self.request.user)

        return render(
            request,
            "notification/notification.html",
            {"notifications": notifications, "lang": get_language()},
        )

    def post(request):
        pass