from django.shortcuts import render, redirect
from accounts.forms import  AuthenticationForm, UserAddressForm, UserProfileForm
from django.contrib.auth import authenticate, login as auth_login , logout as auth_logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
import logging , traceback, pprint
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DeleteView
from .models import UserAddress, UserProfile
from order.models import Order
from braces.views import LoginRequiredMixin

logging.debug('A log message')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            import pdb; pdb.set_trace()
            return redirect(reverse('accounts:login'))
    else:
        form = UserCreationForm()    
    return render(request,'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)
            return HttpResponse('Authenticated successfully')
        else:
            return HttpResponse('Disabled account')
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login.html',{'form':form})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('catalog:booklist')

class AddressListView(LoginRequiredMixin,ListView):
    template_name = 'accounts/address/address_list.html'
    context_object_name = 'addresses'
    model = UserAddress
    paginate_by = 10
    
    def get_queryset(self):
        return UserAddress.objects.filter(user = self.request.user)

class OrderListView(LoginRequiredMixin,ListView):
    template_name = 'accounts/order/order_list.html'
    context_object_name = 'orders'
    model = Order
    
    paginate_by =15
    
    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)

class ProfileCreateView(LoginRequiredMixin,CreateView):
    form_class= UserProfileForm
    template_name='accounts/profile/profile_form.html'
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.user = self.request.user 
        obj.save()
        return HttpResponseRedirect(self.success_url)
    
def profile_detail(request):
    try:
        profile= UserProfile.objects.get(user= request.user) 
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect(reverse_lazy('accounts:profile_new'))
    else:   
        return render(request,'accounts/profile/profile.html',{'profile':profile})
    
    
class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    form_class = UserProfileForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/profile/profile_form.html'
    
    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)


class AddressCreateView(LoginRequiredMixin,CreateView):
    form_class = UserAddressForm
    model = UserAddress
    template_name = 'accounts/address/address_form.html'
    success_url = reverse_lazy('accounts:address_list')
    
    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.user = self.request.user 
        obj.save()
        return HttpResponseRedirect(self.success_url)
    
    
class AddressUpdateView(LoginRequiredMixin,UpdateView):
    form_class = UserAddressForm
    success_url = reverse_lazy('accounts:address_list')
    template_name = 'accounts/address/address_form.html'
    
    def get_object(self, queryset=None):
        return UserAddress.objects.get(user=self.request.user, pk=self.kwargs['pk'])
    '''
    the same as get_from_kwargs(self):
    def form_valid(self, form):
        address = form.save(commit= False)
        address.user = self.request.user
        address.save()
    '''
    
class AddressDeleteView(LoginRequiredMixin,DeleteView):
    form_class = UserAddressForm
    success_url = reverse_lazy('accounts:address_list')
    template_name = 'accounts/address/address_delete.html'
    context_object_name = 'address'
    
    def get_object(self, queryset=None):
        return UserAddress.objects.get(pk=self.kwargs['pk'])

def profile(request):
    user = request.user
    return render(request,'accounts/profile.html', {'user': user})
    



                    
          
            
        