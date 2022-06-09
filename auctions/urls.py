from django.conf import settings
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all",views.all_view,name="all_view"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category",views.category,name="category"),
    path("search/",views.search,name="search"),
    path("search/<word>",views.search2,name="search2"),
    path("mylist/",views.mylist,name="mylist"),
    path("error",views.error,name="error"),
    path("mypage/",views.mypage,name="mypage"),
    path("management/",views.management,name="management"),
    path("newauctions",views.newauctions,name="newauctions"),
    path("item/<id>",views.item,name="item")
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
