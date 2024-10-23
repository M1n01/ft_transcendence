from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from notification.models import UserNotification

import logging

logger = logging.getLogger(__name__)


@method_decorator(login_not_required, name="dispatch")
class Index(TemplateView):
    template_name = "index.html"


# Create your views here.
@login_not_required
def index(request):
    return render(request, "spa/index.html")


class Top(RedirectView):
    url = "/pong/games"
    # template_name = "pong/games.html"


@method_decorator(login_not_required, name="dispatch")
class Nav(TemplateView):
    def get(self, request):

        try:
            user = request.user
            list = UserNotification.objects.filter(
                Q(user=request.user) & Q(is_read=False)
            )
            cnt = len(list) if len(list) > 0 else False
            context = {"hidden": "d-none d-md-none", "cnt_message": cnt}
            if user.is_authenticated:
                context = {"hidden": "", "cnt_message": cnt}

            return render(request, "spa/nav.html", context=context)
        except Exception as e:
            logger.warning(f"Nav Warning:{e}")
            context = {"hidden": "", "cnt_message": 0}
            return HttpResponseBadRequest()
            return render(request, "spa/nav.html", context=context)


@method_decorator(login_not_required, name="dispatch")
class ToLogin(TemplateView):
    template_name = "spa/error.html"


@method_decorator(login_not_required, name="dispatch")
class isLogin(TemplateView):
    def get(self, request):
        user = request.user
        is_redirect = True
        uri = "/login-signup"
        if user.is_authenticated:
            is_redirect = False

        json = {"is_redirect": is_redirect, "uri": uri}
        return JsonResponse(json)


class errorPageView(TemplateView):
    template_name = "spa/error.html"

    def get(self, request):
        request.status = 404
        return render(request, "spa/error.html")
