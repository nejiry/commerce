from email import message
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import forms
from datetime import timezone

from .models import User,auctions,trade,coment


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def category(request):
    return render(request, "auctions/category.html")


def search(request):
    ENT = []
    if request.method == "POST":
        if request.POST["searchword"] is not None:
            TITLE = request.POST["searchword"]
            entries = auctions.objects.all().values("auction_title") 
            ENT.clear()
            for entry in entries:
                if entry in TITLE:
                    ENT.append(entry)
                    return render(request, "auctions/searched.html",{
                       "entries" : ENT
                   })
                           
            if not ENT:
             return render(request, "auctions/Error.html",{
                    "messege": (TITLE) + " SEARCHED BUT NOT IN ITEMS"} )
        
        else:
            return render(request,"auctions/Error.html",{
                "messege" : "ERROR this is GET request"
            })   
    
    else:
        return render(request,"auctions/Error.html",{
            "messege" : "ERROR this is GET request"
        })  


def mylist(request):#お気に入りリスト
    return render(request, "auctions/mylist.html")


def mypage(request):#アカウント情報、
    nowusername = request.user.username#ログイン中のユーザー名を取得
    user_info = User.objects.filter(username=nowusername)
    return render(request, "auctions/mypage.html",{
        "userinfo" : user_info
    })


def error(request):#エラー出力
    return render(request, "auctions/Error.html")


def management(request):#自分が行った投稿、コメントの履歴が見れる
    return render(request, "auctions/management.html")


def newauctions(request):
    if request.method == "POST":
        form = forms.AuctionForm(request)
        if form.is_valid():
            auctions.auction_title = request.POST['auction_title']
            auctions.auction_price = request.POST['auction_price']
            auctions.auction_content = request.POST['auction_content']
            auctions.auction_limittime = request.POST['auction_limittime']
            auctions.auction_picture = request.FILES['auction_picture']
            auctions.auction_exhibitor = request.user
            auctions.auction_daytime = timezone.now()
            return render(request,"auctions/index.html",{
                "message" : "complated"
            })

    else:    
        form = forms.AuctionForm()
        return render(request, "auctions/newauctions.html",{
            'form':form
        })

def item(request):
    return render(request, "auctions/item.html")

