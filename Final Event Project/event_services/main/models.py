# models.py
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensure this line exists
    name = models.CharField(max_length=255)
    description = models.TextField()
    portfolio = models.JSONField(null=True, blank=True)  # Make it optional for now
    pricing = models.JSONField(null=True, blank=True)    # Make it optional for now



    # Additional fields as necessary

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey('main.Vendor', on_delete=models.CASCADE)  # Referencing Vendor
    service = models.ForeignKey('main.Service', on_delete=models.CASCADE)  # Referencing Service
    service_date = models.DateField()
    service_size = models.CharField(max_length=50)
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.vendor.name} on {self.service_date}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('Catering', 'Catering'),
        ('Decoration', 'Decoration'),
        ('Photography', 'Photography'),
        ('Venues', 'Venues'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Keep this one
    description = models.TextField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)  # This should point to Vendor
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/')

    def __str__(self):
        return self.name