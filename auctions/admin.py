from django.contrib import admin
from . models import User,trade,coment,auctions

admin.site.register(User)
admin.site.register(trade)
admin.site.register(coment)
admin.site.register(auctions)

# Register your models here.
