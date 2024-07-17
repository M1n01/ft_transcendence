from django.shortcuts import render
from django.http import HttpResponse
import asyncio
from django.views.generic import TemplateView


# Create your views here.
def index(request):
	return render(request, 'spa/index.html')

# テスト用　後で消す
#def lang(request):
	#return render(request, 'lang_test.html')

#def script(request):
	#return render(request, 'script.html')

#def script2(request):
	#return render(request, 'script2.html')

	