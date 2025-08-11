from django.urls import path
from . import views
urlpatterns = [
    path("books/", views.get_list),
    path("books/<int:id>", views.books_detail),

    path("books/add", views.books_add),

    path("index/", views.index),
]
