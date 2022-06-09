from nis import cat
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import modelformset_factory
from django.core import validators


class User(AbstractUser):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    mylist = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.username},{self.email}"

class trade(models.Model):
    trade_auction_ID = models.IntegerField(unique=True,null=True)
    trade_price = models.IntegerField(validators=[validators.MinValueValidator(0)])
    trade_daytime = models.DateTimeField(null=True)
    trade_bidder = models.CharField(max_length=20,null=True)
    trade_validity = models.BooleanField(default=True,)#購買履歴表示用
    
class coment(models.Model):
    coment_daytime = models.DateTimeField(null=True)
    coment_content = models.TextField()
    coment_user = models.CharField(max_length=20,null=True)
    coment_auction_ID=models.IntegerField(null=True)



class auctions(models.Model):
    LIMIT = (
        ('1','3Hours'),
        ('2','12Hours'),
        ('3','24Hours'),
        ('4','3days'),
    )

    auction_title = models.CharField(max_length=20,null=True)
    auction_exhibitor = models.CharField(max_length=20,null=True)
    auction_price = models.IntegerField(validators=[validators.MinValueValidator(0)],null=True)
    auction_limittime = models.CharField(max_length=1,choices=LIMIT,null=True)
    auction_content = models.TextField(null=True)
    auction_picture = models.ImageField(upload_to="image",blank=True,null=True,default="image/NoImage.jpeg")
    auction_categoli = models.CharField(max_length=10, null=True)
    auction_validity = models.BooleanField(default=True,)#オークションが有効かどうか
    auction_daytime = models.DateTimeField(null=True)