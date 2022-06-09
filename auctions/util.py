from .models import User,auctions,trade,coment
import datetime
from django.utils import timezone


def limittime (limit):
    daytime = limit.auction_daytime.replace(microsecond = 0)
    Limit = limit.auction_limittime
    nowtime = timezone.now().replace(microsecond = 0)
    durations = []

    if Limit == "1":
        durations = (daytime + datetime.timedelta(hours=3)) - nowtime

    elif Limit == "2":
        durations = (daytime + datetime.timedelta(hours=12)) - nowtime

    elif Limit == "3" :
        durations = (daytime + datetime.timedelta(days=1)) - nowtime

    elif Limit == "4":
        durations = (daytime + datetime.timedelta(days=3)) - nowtime
    
    else:
        durations = "NULL"
    
    return durations

def get_comment(id):
    lists = coment.objects.filter(coment_auction_ID = id)
    return lists