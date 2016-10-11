import django
django.setup()

from urllib.request import urlopen
from bs4 import BeautifulSoup
from catalog.models import Category, Book
import re


def clear():
    #clear book and category information
    Book.objects.all().delete()
    Category.objects.all().delete()

def url_generate(i):
    offset = 48*i
    return 'https://www.packtpub.com/all?search=&offset='+ str(offset) +'&rows=48&sort='

def get_book(url,booklist):
    html = urlopen(url)
    soup = BeautifulSoup(html.read(), 'lxml')
    
    # find all div with class name 'book-block'
    book_list = soup.find_all(class_ = 'book-block')
    
    # open json file
 
    for book in book_list:
        book_category = book.find_parent().get('data-product-category')
        book_title = book.find(class_ = 'book-block-title').string.strip()
        book_img = 'http:'+book.img.get('src')
        book_price = book.find_parent().get('data-product-price')
        book_dict = {'title':book_title,'price':book_price,'img_url':book_img,'category':book_category}
        booklist.append(book_dict)

    
def create_category():
    html = urlopen('https://www.packtpub.com/all')
    soup = BeautifulSoup(html.read(), 'lxml')
    
    
    cat_list = soup.find('div','facet-category-main-wrapper category').find_all(class_ = 'facet-cat-text')
    for cat in cat_list:
        cat_name = cat.string.strip()
        cat_name = re.sub(r'\(.*?\)','',cat_name).strip()
        Category.objects.create(name=cat_name)
        
def create_book(books):
    for book in books:
        cat = Category.objects.get(name= book.get('category'))
        Book.objects.create(title=book.get('title'),img_url=book.get('img_url'),price=book.get('price'),category=cat)

clear()
print(Book.objects.count())
create_category()
books =[]
for i in range(0,5):
    url = url_generate(i)
    get_book(url, books)
    print(len(books))
create_book(books)
print(Book.objects.count())
    
    
        