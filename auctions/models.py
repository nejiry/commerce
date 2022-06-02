from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import modelformset_factory


class User(AbstractUser):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    mylist = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.username},{self.email}"

class trade(models.Model):
    trade_price = models.IntegerField()
    trade_daitime = models.DateTimeField(blank=True,null=True)
    trade_bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    
class coment(models.Model):
    coment_daytime = models.DateTimeField(blank=True,null=True)
    coment_content = models.TextField()
    coment_user = models.ForeignKey(User, on_delete=models.CASCADE)


class auctions(models.Model):
    auction_title = models.CharField(max_length=20,null=True)
    auction_exhibitor = models.CharField(max_length=20,unique=True)
    auction_price = models.IntegerField()
    auction_daytime = models.DateTimeField(blank=True,null=True)
    auction_limittime = models.DurationField()
    auction_content = models.TextField()
    auction_picture = models.ImageField(upload_to="image",blank=True,null=True)
    auction_categoli = models.CharField(max_length=10)