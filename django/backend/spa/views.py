from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator


@method_decorator(login_not_required, name="dispatch")
class Index(TemplateView):
    template_name = "index.html"


# Create your views here.
@login_not_required
def index(request):
    return render(request, "spa/index.html")


class Top(TemplateView):
    template_name = "pong/games.html"


@method_decorator(login_not_required, name="dispatch")
class Nav(TemplateView):
    def get(self, request):
        user = request.user
        context = {"hidden": "d-none d-md-none"}
        if user.is_authenticated:
            context = {"hidden": ""}

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
