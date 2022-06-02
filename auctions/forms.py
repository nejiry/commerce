from email import contentmanager
from http.client import PROXY_AUTHENTICATION_REQUIRED
from sre_constants import CATEGORY_LINEBREAK
from turtle import title
from django import forms

from .models import auctions


class AuctionForm(forms.ModelForm):
    class Meta():
        model = auctions
        fields = (
            'auction_title',
            'auction_price',
            'auction_content',
            'auction_categoli',
            'auction_picture')
