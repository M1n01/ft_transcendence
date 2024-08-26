from django.shortcuts import render

# from django.http import HttpResponse
# import asyncio
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator

# from django.contrib.auth.mixins import LoginRequiredMixin


@method_decorator(login_not_required, name="dispatch")
class Index(TemplateView):
    template_name = "index.html"


# Create your views here.
@login_not_required
def index(request):
    return render(request, "spa/index.html")


# テスト用　後で消す
# def lang(request):
# return render(request, 'lang_test.html')

# def script(request):
# return render(request, 'script.html')

# def script2(request):
# return render(request, 'script2.html')
