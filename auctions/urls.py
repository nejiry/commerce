from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category",views.category,name="category"),
    path("search/",views.search,name="search"),
    path("mylist/",views.mylist,name="mylist"),
    path("error",views.error,name="error"),
    path("mypage/",views.mypage,name="mypage"),
    path("management/",views.management,name="management"),
    path("newauctions",views.newauctions,name="newauctions"),
    path("item/",views.item,name="item")
]
