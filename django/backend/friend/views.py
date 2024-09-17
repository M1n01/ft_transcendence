from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy
from .forms import FriendRequestForm, SearchFriendForm
from .models import Friendships, FriendshipsStatusChoices
from accounts.models import FtUser

# from django.db.models import Q
from django.http import (
    # JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    # HttpResponseForbidden,
    HttpResponse,
)
from django.db import IntegrityError
from django.views.generic.edit import UpdateView


# class FriendView(TemplateView):
#    def get(self, request):
#        print("friend get")
#        search_form = SearchFriendForm
#        make_form = MakeFriendForm
#        results = []
#        username = request.GET.get("username", "")
#        print(f"No.1:{username=}")
#        if username:
#            print(f"{username=}")
#            results = FtUser.objects.filter(username__icontains=username)
#            print(f"{results=}")
#
#        return render(
#            request,
#            "friend/friend.html",
#            {"search_form": search_form, "make_form": make_form, "results": results},
#        )
#
#    def post(request):
#        pass


class FriendView(ListView):
    # class FriendView(CreateView):
    model = FtUser
    request_model = Friendships
    template_name = "friend/friend.html"
    context_object_name = "users"
    paginate_by = 10  # ページネーションが必要な場合

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
        # print(f"{not_search=}")

        results = []
        friends = self.get_friendlist()
        not_search2 = friends.values_list("friend", flat=True)
        not_search = not_search1 | not_search2
        # not_search.extend(not_search_tmp)
        # print(f"{not_search_tmp=}")
        # print(f"{not_search=}")
        username = request.GET.get("username", "")
        if username:
            results = FtUser.objects.exclude(id__in=not_search).filter(
                username__icontains=username
            )
            # results = FtUser.objects.filter(username__icontains=username)
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


# Create your views here.
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
    # queryset = Friendships.objects.all()

    def get(self, request):
        print("respond No.1")
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
        print("respond No.1")
        # モデルを保存する
        try:
            print("respond No.2")
            form.save()
            print("respond No.3")
        except Exception:
            print("respond No.4")
            return HttpResponseServerError()
        print("respond No.5")
        return HttpResponse()

    def form_invalid(self, form):
        print("respond No.6")
        return HttpResponseBadRequest()

    pass


# class FriendRequest(TemplateView):
class FriendRequest(CreateView):
    form_class = FriendRequestForm

    # form_class = MakeFriendForm
    template_name = "friend/request.html"
    usable_password = None

    def form_invalid(self, form):
        print("form_invalid")
        pass

    def form_valid(self, form):
        print("form_valid")
        pass

    def get(self, request):
        print("friend request get")
        return render(request, "friend/search.html")

    # success_url = reverse_lazy("friend:friend")
    def post(self, request):
        print("friend request post")
        try:
            username = request.POST.get("username")
            print(f"{username=}")

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

        # src_user = FtTmpUser.objects.get(email=user.email)
        # FtUser.objects.create(
        #
        # )

        # if tmp_res.status_code >= 300 and tmp_res.status_code < 400:
        # print(f"No.3")

        # form.save()
        # tmp_res = super().form_valid(form)
        pass


def make(request):
    return render(request, "friend/request.html")


# def find(request):
# return render(request, "friend/find.html")


# class FriendListView(ListView):
#    # class FriendView(CreateView):
#    model = Friendships
#    # friend_model = Friendships
#    template_name = "friend/list.html"
#    context_object_name = "friends"
#    paginate_by = 10  # ページネーションが必要な場合
#
#    def get_queryset(self):
#        return self.model.objects.filter(user=self.request.user)

# def get(self, request):
#    # print("friend get")
#    search_form = SearchFriendForm
#    make_form = FriendRequestForm
#    friend_request = self.request_model.objects.filter(
#        friend=self.request.user, status=FriendshipsStatusChoices.PENDING
#    )
#    print(f"{len(friend_request)=}")

#    results = []
#    username = request.GET.get("username", "")
#    if username:
#        results = FtUser.objects.filter(username__icontains=username)
#    return render(
#        request,
#        "friend/friend.html",
#        {
#            "search_form": search_form,
#            "make_form": make_form,
#            "results": results,
#            "friend_requests": friend_request,
#        },
#    )
