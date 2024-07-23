from django.shortcuts import render

from django.views.generic import ListView
from .models import Comment


class CommentList(ListView):
    model = Comment


# Create your views here.
