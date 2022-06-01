from email import contentmanager
from http.client import PROXY_AUTHENTICATION_REQUIRED
from sre_constants import CATEGORY_LINEBREAK
from turtle import title
from django import forms


class Form(forms.Form):
    title = forms.CharField(
        max_length=100,
    )
    content= forms.CharField(
        max_length=100,
    )
    picture= forms.CharField(
        max_length=100,
    )
    category= forms.CharField(
        max_length=100,
    )
    price= forms.IntegerField(
        max_length=100,
    )
    limititime= forms.IntegerField()