from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
import os
from urllib.parse import urlparse
from urllib.request import urlretrieve
import random

# Create your models here.
class Book(models.Model):
    title= models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    img_url = models.CharField(max_length=180,null= True, blank = True)
    category = models.ForeignKey('Category',null= True)
    isbn = models.CharField(max_length=14, null= True)
    author = models.CharField(max_length=120, null= True)
    created = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=120,unique=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)
        
    def get_absolute_url(self):
        return reverse('catalog:book_detail',  args=[self.slug,])
    
    
        
    
class Category(models.Model):
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=120, unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('catalog:books_by_category', args=[self.slug,])