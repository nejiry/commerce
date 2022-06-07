from email import message
from django import conf
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import forms,util
from django.utils import timezone
from .models import User,auctions,trade,coment


def index(request):
    Query = auctions.objects.order_by('?')[:5]
    Query = list(Query)
    for entries in Query:
        entries.auction_limittime = util.limittime(entries)
     
    return render(request, "auctions/index.html",{
        "Query" : Query,
    })
    


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
    user_info = User.objects.get(username=nowusername)
    return render(request, "auctions/mypage.html",{
        "info" : user_info
    })


def error(request):#エラー出力
    return render(request, "auctions/Error.html")


def management(request):#自分が行った投稿、コメントの履歴が見れる
    return render(request, "auctions/management.html")


def newauctions(request):
    if request.method == "POST":
        form = forms.AuctionForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.auction_exhibitor = request.user.username
            post.auction_picture = form.cleaned_data['auction_picture']
            post.auction_daytime = timezone.now()
            post.save()
            return render(request,"auctions/index.html",{
                "message" : f"complated {auctions.auction_title}"
            })
        else:
            return render(request,"auctions/index.html",{
                "messege" : "Failed"
            })
    else:    
        form = forms.AuctionForm()
        return render(request, "auctions/newauctions.html",{
            'form':form
        })

def item(request,id):
    if request.method == "POST":
        Bid_Price = request.POST["bid_price"]
        auction = auctions.objects.get(id=id)
        price = auction.auction_price
        if price > Bid_Price:
            return render(request,"auctions/item.html",id,{
                "message" : "Amount is too low.",
            })
       
        else:
            trade_auction_ID = auction
            trade_bidder = request.user.username
            trade_price = Bid_Price
            trade.objects.update_or_create(trade_price, trade_bidder, trade_auction_ID)
            return render(request,"auctions/item.html",id,{
                "message" : "complated",
            })
  
    else:    
        entries = auctions.objects.get(id=id)
        limit = util.limittime(auctions.objects.get(id=id))
        if int(limit.total_seconds()) < 0 :
            return render(request, "auctions/item.html",{
                "message" : "This auctision was Close",
                "limittime" : limit,
                "ent" : entries,
            })
        else:    
            return render(request, "auctions/item.html",{
                "limittime" : limit,
                "ent" : entries,
            })
    
