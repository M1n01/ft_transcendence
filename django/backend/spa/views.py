from django.shortcuts import render

# from django.template import loader
from django.http import JsonResponse

# from django.conf import settings

# from django.http import HttpResponse
# import asyncio
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator

# from django.shortcuts import redirect

# from accounts.oauth import FtOAuth
# from accounts.forms import SignUpForm, LoginForm
# from accounts.views import LoginSignupView

# from django.urls import reverse_lazy

# from accounts.views import LoginSignupView

# from django.contrib.auth.mixins import LoginRequiredMixin


@method_decorator(login_not_required, name="dispatch")
class Index(TemplateView):
    template_name = "index.html"

    # def get(self, request):
    #    user = request.user
    #    if user is None:
    #        return render(request, "spa/index.html")
    #    return render(request, "spa/index.html")


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
            print("Error ")

        return render(request, "spa/nav.html", context=context)
        # return redirect("/spa/nav")
        # return redirect(LoginSignupView)
        # view = LoginSignupView()
        # return view
        # return RedirectView.as_view(url="/accounts/login-signup/")


@method_decorator(login_not_required, name="dispatch")
class ToLogin(TemplateView):
    template_name = "spa/error.html"


@method_decorator(login_not_required, name="dispatch")
class isLogin(TemplateView):
    print("isLogin No.0")

    def get(self, request):
        print("isLogin No.1")
        user = request.user
        is_redirect = True
        uri = "/login-signup"
        print("isLogin No.2")
        if user.is_authenticated:
            is_redirect = False

        json = {"is_redirect": is_redirect, "uri": uri}
        # data = {"is_auth": "is_auth", "html": "content", "uri": uri}
        print("isLogin No.3")
        return JsonResponse(json)


# テスト用　後で消す
# def lang(request):
# return render(request, 'lang_test.html')

# def script(request):
# return render(request, 'script.html')

# def script2(request):
# return render(request, 'script2.html')
