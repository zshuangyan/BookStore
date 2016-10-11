from django.conf.urls import url
from django.contrib.auth.views import login, logout
from .views import register, AddressListView, AddressCreateView, AddressUpdateView, AddressDeleteView, OrderListView, profile_detail, ProfileCreateView, ProfileUpdateView
urlpatterns = [
    url(r'^register/$', register, name='register'),          
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^address/$', AddressListView.as_view(), name='address_list'),
    url(r'^address/new/$', AddressCreateView.as_view(), name='address_new'), 
    url(r'^address/(?P<pk>\d+)/edit/$', AddressUpdateView.as_view(), name='address_edit'),
    url(r'^address/(?P<pk>\d+)/delete/$', AddressDeleteView.as_view(), name='address_delete'),  
    url(r'^order/$', OrderListView.as_view(), name='order_list'), 
    url(r'^profile/new/$', ProfileCreateView.as_view(), name='profile_new'),
    url(r'^profile/edit/$', ProfileUpdateView.as_view(), name='profile_edit'),
    url(r'^profile/$',profile_detail,name='profile')     
               ]