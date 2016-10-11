from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserAddress
from catalog.models import Book
from cart.cart import Cart
import random
import string
# Create your models here.

class Order(models.Model):
    STATUS = (
        (1,'submitted'),
        (2,'shipped'),
        (3,'confirmed'),
    )
    user = models.ForeignKey(User)
    address = models.ForeignKey(UserAddress)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    order_id = models.CharField(max_length=12, editable=False)
    status = models.IntegerField(choices= STATUS, default=1)
    
    def save(self,*args, **kwargs):
        if not self.id:
            self.order_id = ''.join([random.choice(string.ascii_uppercase) for n in range(0,2)])+'-'+''.join([random.choice(string.digits) for n in range(0,10)])
            super().save(*args,**kwargs)
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    def __str__(self):
        return 'Order: '+ str(self.id)
    
        
        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    book = models.ForeignKey(Book)
    quantity = models.PositiveIntegerField()
    
    @property
    def unit_price(self):
        return self.book.price
    
    @property
    def total_price(self):
        return self.quantity*self.unit_price
    
    def __str__(self):
        return self.book.title
    