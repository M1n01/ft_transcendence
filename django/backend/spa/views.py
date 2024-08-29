from django.shortcuts import render

# from django.http import HttpResponse
# import asyncio
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

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


@method_decorator(login_not_required, name="dispatch")
class Top(TemplateView):
    def get(self, request):
        print("Top No.1")
        user = request.user
        if user.is_authenticated:
            print("Error ")
        return redirect("/accounts/login-signup")
        # return redirect(LoginSignupView)
        # view = LoginSignupView()
        # return view
        # return RedirectView.as_view(url="/accounts/login-signup/")


@method_decorator(login_not_required, name="dispatch")
class Nav(TemplateView):
    # template_name = "/spa/nav.html"

    def get(self, request):
        print("spa Nav No.1")
        user = request.user
        print("spa Nav No.2")
        if user.is_authenticated:
            print("Error ")

        print("spa Nav No.3")
        return render(request, "spa/nav.html")
        # return redirect("/spa/nav")
        # return redirect(LoginSignupView)
        # view = LoginSignupView()
        # return view
        # return RedirectView.as_view(url="/accounts/login-signup/")


# テスト用　後で消す
# def lang(request):
# return render(request, 'lang_test.html')

# def script(request):
# return render(request, 'script.html')

# def script2(request):
# return render(request, 'script2.html')
