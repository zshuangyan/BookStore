from django.conf.urls import url
from .views import order_create , order_detail

urlpatterns = [
    url(r'^create/$', order_create, name= 'create'),
    url(r'^(?P<order_id>[\w\-]+)/$', order_detail, name='order_detail'),
               ]