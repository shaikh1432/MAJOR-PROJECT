# admin.py
from django.contrib import admin
from .models import Profile, Vendor, Booking, BlogPost, Service

# Registering Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_vendor')
    search_fields = ('user__username',)
    list_filter = ('is_vendor',)

# Registering Vendor model
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)

# Registering Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_date', 'created_at')
    search_fields = ('user__username', 'vendor__name')
    list_filter = ('service_date', 'created_at')

# Registering BlogPost model
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at', 'updated_at')

# Registering Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'vendor', 'price')
    search_fields = ('name', 'vendor__username')
    list_filter = ('category', 'vendor')

