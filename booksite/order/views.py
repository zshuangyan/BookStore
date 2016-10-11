from django.shortcuts import render, redirect
from order.forms import OrderForm
from cart.cart import Cart
from order.models import OrderItem, Order
from catalog.models import Book
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def order_create(request):
    cart = Cart(request)
    user = request.user
    if request.method == 'POST':
        form= OrderForm(user,request.POST)
        order = form.save(commit = False)
        order.user = user
        order.save()
        for item in cart:
            OrderItem.objects.create(order= order, book = item.book , quantity= item.quantity)
        cart.clear()
        return redirect('order:order_detail', order_id = order.order_id)
    else:
        form = OrderForm(user)
        categories =[]
        for item in cart:
            category = item.book.category
            if category not in categories:
                categories.append(category)
        if categories:
            related_books = Book.objects.filter(category = categories[0])
            if len(categories)>1:
                for category in categories[1:]:
                    related_books= related_books|(Book.objects.filter(category = category))
        related_books = related_books[:5]
        return render(request,'order/order_form.html',{'cart':cart, 'form':form,'related_books':related_books})
    
def order_detail(request, order_id):
    order = Order.objects.get(order_id = order_id)
    items = order.items.all()
    categories =[]
    for item in items:
        category = item.book.category
        if category not in categories:
            categories.append(category)
    if categories:
        related_books = Book.objects.filter(category = categories[0])
        if len(categories)>1:
            for category in categories[1:]:
                related_books= related_books|(Book.objects.filter(category = category))
    related_books = related_books[:5]
    return render(request,'order/order_detail.html',{'order':order,'items':items,'related_books':related_books})
   
