from django.shortcuts import render
from django.views.generic import CreateView, ListView
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
    paginate_by = 2

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
        # not_search1 = friend_request.values_list("friend", flat=True)

        # results = []
        friends = self.get_friendlist()
        # not_search2 = friends.values_list("friend", flat=True)
        # not_search = not_search1 | not_search2
        # username = request.GET.get("username", "")
        # if username:
        #    results = FtUser.objects.exclude(id__in=not_search).filter(
        #        username__icontains=username
        #    )
        return render(
            request,
            "friend/friend.html",
            {
                "search_form": search_form,
                "make_form": make_form,
                # "results": results,
                "friends": friends,
                "friend_requests": friend_request,
            },
        )

    def post(request):
        pass


def get_searched_user(user):
    pass


class FindFriendView(ListView):
    model = Friendships
    context_object_name = "results"
    template_name = "friend/search.html"
    search_form = SearchFriendForm
    paginate_by = 2

    def get_queryset(self):
        friendships = Friendships.objects.filter(user=self.request.user)
        frendshipd_id = [friendship.friend.id for friendship in friendships]
        frendshipd_id.append(self.request.user.id)
        username = self.request.GET.get("username", "")
        queryset = []
        if username:
            queryset = FtUser.objects.exclude(id__in=frendshipd_id).filter(
                username__icontains=username
            )
        return queryset

    def get_context_data(self, **kwargs):
        print("context No.1")
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["query"] = "?username=" + username
        context["search_form"] = self.search_form
        print("context No.2")
        return context


# def get(request):
#   form = SearchFriendForm()
#   results = []
#   query = request.GET.get("query", "")
#   if query:
#       results = FtUser.objects.filter(username__icontains=query)
#
#   return render(request, "friend/search.html", {"form": form, "results": results})


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
            print("friend request No.1")
            username = request.POST.get("username")
            message = request.POST.get("request-message")
            print(f"friend request No.2:{username=}")
            print(f"friend request No.2:{message=}")
            tmp_friend = FtUser.objects.get(username=username)
            print("friend request No.3")
            if tmp_friend is None:
                print("friend request No.4")
                return HttpResponseBadRequest()
            print("friend request No.5")

            Friendships.objects.create(
                user=request.user, friend=tmp_friend, message=message
            )
            print("friend request No.6")
            return HttpResponse()

        except IntegrityError as e:
            print(f"Copy Error:{e}")
        except Exception as e:
            print(f"Copy Error:{e}")
        return HttpResponseBadRequest()


def make(request):
    return render(request, "friend/request.html")


class RequestsView(ListView):
    model = Friendships
    context_object_name = "requests"
    search_form = SearchFriendForm
    template_name = "friend/requests.html"
    paginate_by = 2

    def get_queryset(self):
        return self.model.objects.filter(
            friend=self.request.user, status=FriendshipsStatusChoices.PENDING
        )

    # def get_context_data(self, **kwargs):
    #    print("context No.1")
    #    context = super().get_context_data(**kwargs)
    #    username = self.request.GET.get("username", "")
    #    context["query"] = "?username=" + username
    #    print("context No.2")
    #    return context
