from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.show_wiki,name="show_wiki"),
    path("search/",views.search,name="search")
]
