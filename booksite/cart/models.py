from django.db import models
from catalog.models import Book
import string
import random

class Cart(models.Model):
    cart_id = models.CharField(max_length=32, editable = False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    check_out = models.BooleanField(default= False)
    def save(self,*args, **kwargs):
        if not self.id:
            self.cart_id = ''.join([random.choice(string.ascii_letters+string.digits) for n in range(0,32)])
            super().save(*args,**kwargs)
            
    def __str__(self):
        return 'Cart: ' + str(self.cart_id)
    
class Item(models.Model):
    cart = models.ForeignKey(Cart)
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
    

    
    

