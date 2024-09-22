from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy
from .forms import FriendRequestForm, SearchFriendForm
from .models import Friendships, FriendshipsStatusChoices
from accounts.models import FtUser

from django.http import (
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponse,
)
from django.db import IntegrityError
from django.views.generic.edit import UpdateView


class FriendView(ListView):
    model = FtUser
    request_model = Friendships
    template_name = "friend/friend.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        username = self.request.GET.get("username", "")
        if username:
            queryset = FtUser.objects.filter(username__icontains=username)
        return queryset

    def get_friendlist(self):
        return Friendships.objects.filter(
            user=self.request.user,
            status=FriendshipsStatusChoices.ACCEPTED,
        )

    def get(self, request):
        # print("friend get")
        search_form = SearchFriendForm
        make_form = FriendRequestForm
        friend_request = self.request_model.objects.filter(
            friend=self.request.user, status=FriendshipsStatusChoices.PENDING
        )
        not_search1 = friend_request.values_list("friend", flat=True)

        results = []
        friends = self.get_friendlist()
        not_search2 = friends.values_list("friend", flat=True)
        not_search = not_search1 | not_search2
        username = request.GET.get("username", "")
        if username:
            results = FtUser.objects.exclude(id__in=not_search).filter(
                username__icontains=username
            )
        return render(
            request,
            "friend/friend.html",
            {
                "search_form": search_form,
                "make_form": make_form,
                "results": results,
                "friends": friends,
                "friend_requests": friend_request,
            },
        )

    def post(request):
        pass


class FindFriendView(TemplateView):
    template_name = "friend/search.html"

    def get(request):
        form = SearchFriendForm()
        results = []
        query = request.GET.get("query", "")
        if query:
            results = FtUser.objects.filter(username__icontains=query)

        return render(request, "friend/search.html", {"form": form, "results": results})


class RespondFriendRequest(UpdateView):
    model = Friendships
    fields = ["id", "status"]
    template_name = "friend/friend.html"  # 使わない
    success_url = reverse_lazy("friend:friend")

    def get(self, request):
        return HttpResponse()

    def post(self, request):
        id = request.POST.get("id")
        status = request.POST.get("status")
        friendship = self.model.objects.get(id=id)
        friendship.status = status
        friendship.save()

        Friendships.objects.create(
            user=self.request.user, friend=friendship.user, status=status
        )

        return HttpResponse()

    def form_valid(self, form):
        try:
            form.save()
        except Exception:
            return HttpResponseServerError()
        return HttpResponse()

    def form_invalid(self, form):
        return HttpResponseBadRequest()

    pass


# class FriendRequest(TemplateView):
class FriendRequest(CreateView):
    form_class = FriendRequestForm
    template_name = "friend/request.html"
    usable_password = None

    def form_invalid(self, form):
        pass

    def form_valid(self, form):
        pass

    def get(self, request):
        return render(request, "friend/search.html")

    # success_url = reverse_lazy("friend:friend")
    def post(self, request):
        try:
            username = request.POST.get("username")
            tmp_friend = FtUser.objects.get(username=username)
            if tmp_friend is None:
                return HttpResponseBadRequest()

            Friendships.objects.create(user=request.user, friend=tmp_friend)
            return HttpResponse()

        except IntegrityError as e:
            print(f"Copy Error:{e}")
        except Exception as e:
            print(f"Copy Error:{e}")
        return HttpResponseBadRequest()


def make(request):
    return render(request, "friend/request.html")
