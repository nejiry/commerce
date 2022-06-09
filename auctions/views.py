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
    entries=auctions.objects.all()
    for entry in entries:
        limit = util.limittime(entry)
        if int(limit.total_seconds()) < 0 :
            entry.auction_validity = False
            entry.save()
    Query = auctions.objects.filter(auction_validity = True).order_by('?')[:5]
    Query = list(Query)
    for entries in Query:
        entries.auction_limittime = util.limittime(entries)
     
    return render(request, "auctions/index.html",{
        "Query" : Query,
        "message" : "5 Active Auctions"
    })

def all_view(request):
    Query = auctions.objects.order_by('?')[:10]
    Query = list(Query)
    for entries in Query:
        entries.auction_limittime = util.limittime(entries)
     
    return render(request, "auctions/index.html",{
        "Query" : Query,
        "message" : "10 Random Auctions"

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
    lists = []
    category_list = auctions.objects.distinct().values('auction_categoli')
    for category in category_list :
        cat = category['auction_categoli']
        counts = auctions.objects.filter(auction_categoli = cat).count()
        count = {'count': counts} 
        category = category | count
        lists.append(category)
    return render(request, "auctions/category.html",{
        "category" : lists,
        })


def search(request,):
    if request.method == "POST":
        word = request.POST["searchword"]
        result = auctions.objects.filter(auction_title__contains = word)
        for entries in result:
            entries.auction_limittime = util.limittime(entries)
        return render(request, "auctions/index.html",{
            "Query" : result,
            "message" : f"[{word}] Searched" 
    })

def search2(request,word):
        result = auctions.objects.filter(auction_categoli = word).order_by('auction_validity').reverse()
        for entries in result:
            entries.auction_limittime = util.limittime(entries)
        return render(request, "auctions/index.html",{
            "Query" : result,
            "message":"From Category"
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
    trade_log = trade.objects.filter(trade_bidder = request.user.username)
    for log in trade_log:
        entry = auctions.objects.get(id = log.trade_auction_ID)
        limit = util.limittime(entry)
        if int(limit.total_seconds()) < 0 :
            log.auction_validity = False
            log.trade_validity = False
    
    
    comment_log = coment.objects.filter(coment_user = request.user.username)

    return render(request, "auctions/management.html",{
            "trades" : trade_log,
            "comment" : comment_log
    })


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
    entries = auctions.objects.get(id=id)
    limit = util.limittime(entries)
    com_list = coment.objects.filter(coment_auction_ID = id)
    if request.method == "POST":
        if 'bid' in request.POST:
            Bid_Price = int(request.POST["bid_price"])
            price = entries.auction_price
            if price > Bid_Price:
                return render(request,"auctions/item.html",{
                    "message" : "Amount is too low.",
                    "limittime" : limit,
                    "ent" : entries,
                    "lists" : com_list
                })
            else:
                trade.objects.update_or_create(
                trade_auction_ID = id,
                defaults = {
                    "trade_bidder" : request.user.username,
                    "trade_price" : Bid_Price,
                    "trade_daytime" : timezone.now()
                })            
                entries.auction_price = Bid_Price
                entries.save()

                return render(request,"auctions/item.html",{
                    "message" : "complated",
                    "limittime" : limit,
                    "ent" : entries,
                    "lists" : com_list
                })
        else:
            comment = request.POST["comment"]
            coment.objects.create(
                coment_auction_ID = id,
                coment_user = request.user.username,
                coment_content = comment,
                coment_daytime = timezone.now()
            )
            return render(request,"auctions/item.html",{
                    "message" : comment,
                    "limittime" : limit,
                    "ent" : entries,
                    "lists" : com_list,
                })
  
    else:    
        if int(limit.total_seconds()) < 0 :
            return render(request, "auctions/item.html",{
                "message" : "This Auction Has Closed",
                "close_form": "a",
                "limittime" : limit,
                "ent" : entries,
                "lists" : com_list
            })
        else:
            return render(request, "auctions/item.html",{
                "limittime" : limit,
                "ent" : entries,
                "lists" : com_list
            })

