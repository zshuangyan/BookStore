from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from .models import UserAddress, UserProfile
from django.core.files.images import get_image_dimensions
from django.forms.widgets import FileInput
'''
class RegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': "A user with that username already exists.",
        'password_mismatch':"The two password fields didn't match.",
        }
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='password (again)', widget= forms.PasswordInput,
                help_text = "Enter the same password as above, for verification.")
    class Meta:
        model = User
        fields = ['username',]
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'],
                                    code = 'duplicate_username',)          
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'],
                                        code = 'password_mismatch',)
        return self.cleaned_data
'''
class UserProfileForm(forms.ModelForm):
    image = forms.ImageField(label='image',required=False, \
                                    error_messages ={'invalid':"Image files only"},\
                                    widget=FileInput)
    
    class Meta:
        model = UserProfile
        widget={
            'birth': forms.DateInput(attrs={'class':'datepicker'}),
        }
        exclude = ['age','user']
    
        
class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    error_messages = {
        'invalid_login':'Username or password wrong.',
        'inactive':'Account is inactive.',
    }
    def __init__(self,request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username=username,password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_message['invalid_login'],
                                            code = 'invalid_login',)
            if not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'],
                                            code = 'inactive',)
        return self.cleaned_data
    
    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None
    
    def get_user(self):
        return self.user_cache
    
    
class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ['user']
    
            