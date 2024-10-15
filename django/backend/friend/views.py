from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.db.models import Q
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


def get_friendlist(request):
    return Friendships.objects.filter(
        user=request.user,
        status=FriendshipsStatusChoices.ACCEPTED,
    )


def get_blocklist(request):
    return Friendships.objects.filter(
        user=request.user,
        status=FriendshipsStatusChoices.BLOCK,
    )


class FriendView(ListView):
    model = FtUser
    request_model = Friendships
    template_name = "friend/friend.html"
    context_object_name = "users"
    paginate_by = 2

    def get_queryset(self):
        username = self.request.GET.get("username")
        if username:
            queryset = FtUser.objects.filter(username__icontains=username)
        return queryset

    def get(self, request):
        search_form = SearchFriendForm
        make_form = FriendRequestForm
        friend_request = self.request_model.objects.filter(
            friend=self.request.user, status=FriendshipsStatusChoices.PENDING
        )[:4]
        friends = get_friendlist(self.request)[:4]
        blocks = get_blocklist(self.request)[:4]
        return render(
            request,
            "friend/friend.html",
            {
                "search_form": search_form,
                "make_form": make_form,
                "friends": friends,
                "blocks": blocks,
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
        print("test getqueryset No.1")
        friendships = Friendships.objects.filter(
            Q(user=self.request.user) | Q(friend=self.request.user)
        )
        for friend_test in friendships:
            print(f"{friend_test=}")
        # frendshipd_id = [friendship.friend.id for friendship in friendships]
        # フレンド関係にある人はすべて表示させない
        friend_id = [friendship.friend.id for friendship in friendships]
        user_id = [friendship.user.id for friendship in friendships]
        frendshipd_id = friend_id + user_id
        frendshipd_id.append(self.request.user.id)
        username = self.request.GET.get("username")
        queryset = []
        if username:
            queryset = FtUser.objects.exclude(id__in=frendshipd_id).filter(
                username__icontains=username
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["query"] = "?username=" + username
        context["search_form"] = self.search_form
        return context


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

        if status == FriendshipsStatusChoices.BLOCKED:
            print("Friend Status No.1")
            status = FriendshipsStatusChoices.BLOCK

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


class FriendRequest(CreateView):
    form_class = FriendRequestForm
    usable_password = None

    def form_invalid(self, form):
        pass

    def form_valid(self, form):
        pass

    def get(self, request):
        return render(request, "friend/search.html")

    def post(self, request):
        try:
            user_id = request.POST.get("userid")
            message = request.POST.get("request-message")

            friendship = Friendships.objects.get(
                Q(user=user_id) & Q(friend=request.user)
            )
            if friendship is not None:
                return HttpResponseBadRequest()

            tmp_friend = FtUser.objects.get(id=user_id)
            if tmp_friend is None:
                return HttpResponseBadRequest()

            Friendships.objects.create(
                user=request.user, friend=tmp_friend, message=message
            )
            return HttpResponse()

        except IntegrityError as e:
            print(f"Copy Error:{e}")
        except Exception as e:
            print(f"Copy Error:{e}")
        return HttpResponseBadRequest()


class RequestsView(ListView):
    model = Friendships
    context_object_name = "requests"
    # search_form = SearchFriendForm
    template_name = "friend/request-list.html"
    paginate_by = 2

    def get_queryset(self):
        return self.model.objects.filter(
            friend=self.request.user, status=FriendshipsStatusChoices.PENDING
        )


class FriendsView(ListView):
    model = Friendships
    context_object_name = "friends"
    template_name = "friend/friend-list.html"
    paginate_by = 2

    def get_queryset(self):
        return get_friendlist(self.request)


class BlocksView(ListView):
    model = Friendships
    context_object_name = "blocks"
    template_name = "friend/block-users-list.html"
    paginate_by = 2

    def get_queryset(self):
        return get_blocklist(self.request)
