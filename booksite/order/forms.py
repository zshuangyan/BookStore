from .models import Order
from django import forms
from accounts.models import UserAddress
class OrderForm(forms.ModelForm):
    address = forms.ModelChoiceField(queryset=None)
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['address'].queryset=UserAddress.objects.filter(user=user.id)
        self.initial['address']= UserAddress.objects.get(user=user.id, default=True)
                       
    class Meta:
        model = Order
        exclude = ['user','order_id','status']