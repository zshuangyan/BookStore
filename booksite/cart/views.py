from django.shortcuts import render
from cart.cart import Cart
from catalog.models import Book
from django.http.response import  HttpResponse
def show_cart(request):
    cart = Cart(request)
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            item_id = postdata['item_id']
            cart.remove(item_id = item_id)
        if postdata['submit'] == 'Update':
            item_id = postdata['item_id']
            quantity = postdata['quantity']
            cart.update(item_id = item_id, quantity=quantity)    
    return render(request, 'cart/cart.html',{'cart':cart})


    

