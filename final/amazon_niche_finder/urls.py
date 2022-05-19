from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all-categories", views.show_categories, name="show_categories"),
    path("check-keyword", views.check_keyword, name="check_keyword"),
    path("kw-details", views.check_keyword, name="check_keyword"),
    path("search-results/<str:q>", views.search_results,
         name="search_results"),
    path("cat-details/<int:id>", views.show_subcats, name="show_subcats"),
    path("get-bestseller/<int:id>",
         views.get_bestseller,
         name="get_bestseller"),
]
