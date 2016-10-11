from booksite.settings import SESSION_CART_ID
from cart import models
from catalog.models import Book

class ItemDoesNotExist(Exception):
    pass

class Cart():
    def __init__(self,request):
        cart_id = request.session.get(SESSION_CART_ID)
        if cart_id:
            try:
                self.cart = models.Cart.objects.get( cart_id = cart_id , check_out = False)
            except models.Cart.DoesNotExist:
                self.cart = self.new(request)
        else:
            self.cart = self.new(request)
    
    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item
        
    def new(self,request):
        cart = models.Cart.objects.create()
        request.session[SESSION_CART_ID]=cart.cart_id
        return cart
        
    def add(self, book , quantity=1):
        try:
            item = models.Item.objects.get(book = book, cart = self.cart)
        except models.Item.DoesNotExist:
            item = models.Item()
            item.book = book
            item.cart = self.cart
            item.quantity = quantity
            item.save()
        else:
            item.quantity += quantity
            item.save()
                   
    def remove(self, item_id):
        try:
            item = models.Item.objects.get(id = item_id)
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()
                
    def update(self, item_id , quantity = 1):
        try:
            item = models.Item.objects.get(id = item_id)
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            if quantity==0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()  

    
    @property    
    def sub_price(self):
        sub_price = 0
        for item in self.cart.item_set.all():
            sub_price += item.total_price
        return sub_price
    
    def sub_amount(self):
        return self.cart.item_set.all().count()
    
    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()
            