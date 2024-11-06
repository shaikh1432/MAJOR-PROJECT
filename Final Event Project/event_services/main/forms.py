# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BlogPost,Service,Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service_date', 'service_size', 'special_requests']




class SignUpForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('vendor', 'Vendor'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'description', 'price', 'image']