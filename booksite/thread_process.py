import django
django.setup()

import queue
import threading
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from catalog.models import Category, Book
import json
import re

queue = queue.Queue()
books =[]

def clear():
    #clear book and category information
    Book.objects.all().delete()
    Category.objects.all().delete()
    
def create_category():
    html = urlopen('https://www.packtpub.com/all')
    soup = BeautifulSoup(html.read(), 'lxml')
    
    
    cat_list = soup.find('div','facet-category-main-wrapper category').find_all(class_ = 'facet-cat-text')
    for cat in cat_list:
        cat_name = cat.string.strip()
        cat_name = re.sub(r'\(.*?\)','',cat_name).strip()
        Category.objects.create(name=cat_name)
        
def add_attribute_on_book():
    for book in books:
        b = Book.objects.get(title=book.get('title'))
        b.author = book.get('author')
        b.isbn = book.get('isbn')
        b.created = book.get('created')
        b.save()
        
    
def url_generate(i):
    offset = 48*i
    return 'https://www.packtpub.com/all?search=&offset='+ str(offset) +'&rows=48&sort='

def bookhref_generate(url, bookhref_list):
    html = urlopen(url)
    soup = BeautifulSoup(html.read(),'lxml')
    
    # find all div with class name 'book-block'
    book_list = soup.find_all(class_ = 'book-block')
 
    # get link of book
    for book in book_list:
        book_href = 'https://www.packtpub.com'+book.find('a')['href']
        bookhref_list.append(book_href)
        
def get_book_information(url,books):
    req = urllib.request.Request(url)
    try:
        req.selector.encode('ascii')
    except UnicodeEncodeError:
        req.selector = urllib.parse.quote(req.selector)
    response = urllib.request.urlopen(req, timeout=30)
    page = response.read().decode('utf-8')
    soup = BeautifulSoup(page,'lxml')
    
    #book title, isbn, author, img_url
    book_title = soup.find(class_='book-top-block-info-title float-left').h1.string.strip()
    print(book_title)
    book_isbn = soup.find(class_='book-info-isbn13').find(attrs={'itemprop':'isbn'}).string
    book_author = soup.find(class_="book-top-block-info-authors left").contents[0].string.strip()
    book_img_url = soup.find(class_='bookimage').get('src')
    book_category = soup.find(class_='book-top-addtocart').find(attrs={'data-product':'true'}).get('data-product-category').strip()        
    
    #book price like '$48.2' 
    book_price = float(soup.find(attrs={'itemprop':'price'}).get('content'))

    #created time
    date_string = soup.time['datetime']
    book_created = datetime.strptime(date_string,'%Y-%m-%d').date()
    
    book_dict = {'title':book_title, 'isbn':book_isbn, 'author':book_author, 'img_url':book_img_url, 'price':book_price, 'created':book_created,
                 'category':book_category}
    books.append(book_dict)     
    
def worker():
    while True:
        url = queue.get()
        get_book_information(url, books)
        queue.task_done()


clear()
create_category()
for i in range(0,5):
    #get url of page i
    url = url_generate(i)
    
    #get href of each book on page i, save in href_list 
    href_list = []
    bookhref_generate(url, href_list)
    
    #spawn a pool of threads, and pass them queue instance
    for i in range(0,48):
        t = threading.Thread(target=worker)
        t.setDaemon(True)
        t.start()
    
    #populate queue with data
    for href in href_list:
        queue.put(href)
        
    #block until all tasks are done
    queue.join()
print('done')
with open('books.json', 'w') as f:
    json.dump(books, f)
add_attribute_on_book()

    


        

        
        
    
    

        
    
            
