from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from datetime import date

# Create your models here.
class UserAddress(models.Model):
    user = models.ForeignKey(User, related_name='address')
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=12)
    country = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    postcode = models.CharField(max_length=6)
    default = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.default:
            try:
                temp = UserAddress.objects.get(user=self.user, default=True)
            except UserAddress.DoesNotExist:
                pass
            else:
                temp.default = False
                temp.save()
        super().save(*args,**kwargs)
    
    def __str__(self):
        return str(self.country)+' '+str(self.city)+' '+str(self.street)
    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]
    
    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        fields = []
        for f in self._meta.fields:
            fname = f.name        
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_'+fname+'_display'
            if hasattr( self, get_choice):
                value = getattr( self, get_choice)()
            else:
                try :
                    value = getattr(self, fname)
                except UserAddress.DoesNotExist:
                    value = None

            # only display fields with values and skip some fields entirely
            if f.editable and value and f.name not in ('id', 'user') :

                fields.append(
                    {
                   'label':f.verbose_name, 
                   'name':f.name, 
                   'value':value,
                    }
                )
        return fields

class UserProfile(models.Model):
    SEX = (
        (1,'male'),
        (2,'female'),
    )
    user = models.OneToOneField(User,related_name='profile')
    sex = models.IntegerField(choices=SEX,default=1)
    birth = models.DateField()
    age = models.IntegerField()
    company = models.CharField(max_length=120)
    image = models.FileField(null= True, blank= True,upload_to='profile')
    
    def str(self):
        return self.user.username
    
    def save(self,*args,**kwargs):
        today = date.today()
        self.age = today.year - self.birth.year -( (today.month, today.day) < (self.birth.month, self.birth.day) )
        super().save(*args,**kwargs)
    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]
    
    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        fields = []
        for f in self._meta.fields:
            fname = f.name        
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_'+fname+'_display'
            if hasattr( self, get_choice):
                value = getattr( self, get_choice)()
            else:
                try :
                    value = getattr(self, fname)  
                except UserProfile.DoesNotExist:
                    value = None

            # only display fields with values and skip some fields entirely
            if f.name not in ('id', 'user','image') :
                fields.append(
                    {
                   'label':f.verbose_name, 
                   'name':f.name, 
                   'value':value,
                    }
                )
        return fields
    
    
    
            
            
    
