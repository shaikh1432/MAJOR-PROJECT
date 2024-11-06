from django.contrib import admin
from django.urls import path
from main import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Route for the homepage
    path('home', views.home, name='home'),  # Route for the homepage
    path('vendor/<str:vendor_name>/', views.vendor_details, name='vendor_details'),  # New URL for vendor details
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('booking/success/', views.booking_success, name='booking_success'), 
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('dashboard/vendor/add-service/', views.add_service, name='add_service'),  
    path('blog/new/', views.create_blog_post, name='create_blog_post'),
    path('blog/<int:post_id>/', views.blog_post_detail, name='blog_post_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    
    #path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('catering/', views.catering_services, name='catering_services'),
    path('decoration/', views.decoration_services, name='decoration_services'),
    path('photography/', views.photography_services, name='photography_services'),
    path('venues/', views.venues_services, name='venues_services'),
    path('booking_success/', views.booking_success, name='booking_success'),
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)