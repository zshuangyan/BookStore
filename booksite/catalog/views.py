from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView , ListView
from .models import Category, Book
from django.views.generic.edit import FormView
from cart.forms import CartAddProductForm
from django.core.urlresolvers import reverse
from cart.cart import Cart
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.  
def book_list(request):
    categories = Category.objects.filter(is_active= True)
    book_list = Book.objects.filter(is_active= True)
    
    #set item amount in one page
    paginator = Paginator(book_list,12)
    
    #get page number from url
    page = request.GET.get('page')
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request,'catalog/book_list.html',{'categories':categories,'books':books})

class CategoryBookList(ListView):
    template_name = 'catalog/book_list.html'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Book.objects.filter(category=self.category)
    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        book_list = Book.objects.filter(is_active= True)
        paginator = Paginator(book_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            context['books'] = paginator.page(page)
        except PageNotAnInteger:
            context['books'] = paginator.page(1)
        except EmptyPage:
            context['books'] = paginator.page(paginator.num_pages)
        return context    
'''        
class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    slug_url_kwarg = 'slug'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']= Category.objects.filter(is_active=True)
        return context
'''
    
def book_detail(request,slug):
    book = get_object_or_404(Book, slug= slug)
    categories = Category.objects.filter(is_active=True)
    related_books = Book.objects.filter(category=book.category)
    
    #delete oneself from the filter result and get the first four result
    related_books = related_books.exclude(id = book.id)[:4]
    
    form = CartAddProductForm()
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        '''import pdb; pdb.set_trace()'''
        if form.is_valid():
            cd = form.cleaned_data
            cart = Cart(request)
            cart.add( book= book ,quantity = cd['quantity'])
            return HttpResponseRedirect(reverse('cart:show_cart'))
    else:
        return render(request,'catalog/book_detail.html',{'book':book,'related_books':related_books,'categories':categories,'form':form})
        
    
        
    