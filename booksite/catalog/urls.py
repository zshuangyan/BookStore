from django.conf.urls import url
from .views import book_list, CategoryBookList ,book_detail

urlpatterns = [
    url(r'^$', book_list, name='book_list'),
    url(r'^(?P<slug>[\w\-]+)/$', book_detail , name='book_detail'),
    url(r'^categories/(?P<slug>[\w\-]+)/$', CategoryBookList.as_view(), name='books_by_category'),
    ]
