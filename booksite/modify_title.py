import django
django.setup()
from catalog.models import Book
books = Book.objects.all()
for book in books:
    book.description='The book will also teach you to create well designed architectures and increase the performance of current applications'
    book.save()
