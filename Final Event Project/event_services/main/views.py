from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .models import Vendor, Booking,Profile,User,BlogPost,Service
from .forms import BookingForm,SignUpForm,BlogPostForm,ServiceForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from datetime import datetime
# Create your views here.


def home(request):
    
    # Fetch latest blog posts
    latest_posts = BlogPost.objects.all().order_by('-created_at')[:3]

    # Render the 'home.html' template
    return render(request, 'home.html', {
        
        'latest_posts': latest_posts,
    })


def catering_services(request):
    catering_services = Service.objects.filter(category='Catering')
    print("Catering Services:", catering_services)  # Debug output
    return render(request, 'catering_services.html', {'catering_services': catering_services})

def decoration_services(request):
    decoration_services = Service.objects.filter(category='Decoration')
    return render(request, 'decoration_services.html', {'decoration_services': decoration_services})

def photography_services(request):
    photography_services = Service.objects.filter(category='Photography')
    return render(request, 'photography_services.html', {'photography_services': photography_services})

def venues_services(request):
    venue_services = Service.objects.filter(category='Venues')
    return render(request, 'venues_services.html', {'venue_services': venue_services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)  # Fetch the specific service
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.vendor = service.vendor
            booking.service = service
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm()  # Instantiate an empty form for GET request

    return render(request, 'service_detail.html', {'form': form, 'service': service})
    
def booking_success(request):
    return render(request, 'booking_success.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.profile.is_vendor = (form.cleaned_data['user_type'] == 'vendor')
            user.profile.save()
            
            if user.profile.is_vendor:
                # Use get_or_create to ensure the Vendor profile is created only if it doesn't already exist
                vendor, created = Vendor.objects.get_or_create(user=user, defaults={'name': user.username})
                if created:
                    print(f"Vendor profile created for user {user.username}")
                else:
                    print(f"Vendor profile already exists for user {user.username}")

            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

def vendor_details(request, vendor_name):
    # Sample vendor data (this would ideally come from the database)
    vendor_data = {
        'Delicious Catering Co.': {
            'description': 'Top-notch catering services for all events.',
            'portfolio': ['catering1_portfolio1.jpg', 'catering1_portfolio2.jpg'],
            'pricing': {'Small': 100, 'Medium': 150, 'Large': 200},
            'reviews': [{'user': 'John', 'rating': 5, 'comment': 'Excellent service!'}]
        },
        'Gourmet Chefs': {
            'description': 'Premium gourmet catering for weddings and corporate events.',
            'portfolio': ['gourmet_chefs1.jpg', 'gourmet_chefs2.jpg'],
            'pricing': {'Small': 120, 'Medium': 180, 'Large': 250},
            'reviews': [{'user': 'Alice', 'rating': 4, 'comment': 'Great food and presentation.'}]
        },
        'Elegant Events': {
            'description': 'Elegant decorations for every occasion.',
            'portfolio': ['decoration1_portfolio1.jpg', 'decoration1_portfolio2.jpg'],
            'pricing': {'Small': 80, 'Medium': 120, 'Large': 180},
            'reviews': [{'user': 'Alice', 'rating': 4, 'comment': 'Beautiful setup!'}]
        },
        'Festive Decorators': {
            'description': 'Professional decoration services for weddings and corporate events.',
            'portfolio': ['decoration1.jpg', 'decoration2.jpg'],
            'pricing': {'Small': 150, 'Medium': 250, 'Large': 350},
            'reviews': [{'user': 'Jane', 'rating': 4, 'comment': 'Great decorations!'}]
        },
        'Photography Pros': {
            'description': 'Professional photography services for events.',
            'portfolio': ['photography1_portfolio1.jpg', 'photography1_portfolio2.jpg'],
            'pricing': {'Small': 200, 'Medium': 350, 'Large': 500},
            'reviews': [{'user': 'Bob', 'rating': 5, 'comment': 'Amazing pictures!'}]
        },
        'Capture Moments': {
            'description': 'Professional photography services for all your events.',
            'portfolio': ['photography1_portfolio1.jpg', 'photography1_portfolio2.jpg'],
            'pricing': {'Small': 150, 'Medium': 200, 'Large': 300},
            'reviews': [{'user': 'Alice', 'rating': 4, 'comment': 'Great photos!'}]
        },
        'Memories in Focus': {
            'description': 'Professional photography to capture your special moments.',
            'portfolio': ['photography1_portfolio1.jpg', 'photography1_portfolio2.jpg'],
            'pricing': {'Small': 200, 'Medium': 300, 'Large': 500},
            'reviews': [{'user': 'Anna', 'rating': 4, 'comment': 'Great photos, but a bit expensive.'}]
        },
        'Venues Galore': {
            'description': 'Beautiful venues for any event.',
            'portfolio': ['venue1_portfolio1.jpg', 'venue1_portfolio2.jpg'],
            'pricing': {'Small': 300, 'Medium': 500, 'Large': 700},
            'reviews': [{'user': 'Sarah', 'rating': 4, 'comment': 'Great place!'}]
        },
        'Grand Hall': {
            'description': 'Spacious and elegant venue for all occasions.',
            'portfolio': ['grand_hall_portfolio1.jpg', 'grand_hall_portfolio2.jpg'],
            'pricing': {'Small': 500, 'Medium': 700, 'Large': 1000},
            'reviews': [{'user': 'Anna', 'rating': 4, 'comment': 'Beautiful venue!'}]
        },
        'Cozy Cottage': {
            'description': 'Beautiful venue with a warm and inviting atmosphere.',
            'portfolio': ['venue1_portfolio1.jpg', 'venue1_portfolio2.jpg'],
            'pricing': {'Small': 300, 'Medium': 500, 'Large': 700},
            'reviews': [{'user': 'Emily', 'rating': 4, 'comment': 'Lovely venue for a small wedding.'}]
        },
        # Add other vendors similarly
    }
    
    vendor = vendor_data.get(vendor_name)

    if vendor is None:
        return render(request, '404.html', status=404)

    if request.method == 'POST':
        # Here, handle the booking logic (e.g., save to database, send confirmation)
        service_size = request.POST.get('service_size')
        service_date = request.POST.get('service_date')
        special_requests = request.POST.get('special_requests')
        
        # Simulate booking confirmation
        return render(request, 'booking_confirmation.html', {
            'vendor_name': vendor_name,
            'service_size': service_size,
            'service_date': service_date,
            'special_requests': special_requests
        })

    return render(request, 'vendor_details.html', {'vendor_name': vendor_name, **vendor})

@login_required
def vendor_detail(request, vendor_name):
    vendor = get_object_or_404(Vendor, name=vendor_name)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking(
                user=request.user,
                vendor=vendor,
                service_date=form.cleaned_data['service_date'],
                service_size=form.cleaned_data['service_size'],
                special_requests=form.cleaned_data['special_requests']
            )
            booking.save()
            return redirect('booking_confirmation', booking_id=booking.id)  # Redirect to confirmation page
    else:
        form = BookingForm()

    return render(request, 'vendor_detail.html', {
        'vendor_name': vendor.name,
        'description': vendor.description,
        'portfolio': vendor.portfolio,  # Assuming this is a field on Vendor
        'pricing': vendor.pricing,  # Assuming pricing is a dict field
        'reviews': vendor.reviews.all(),  # Assuming this is a related field
        'form': form
    })

# views.py (add this at the end)
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {
        'booking': booking
    })

@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {
        'bookings': bookings
    })

@login_required 
def vendor_dashboard(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        return render(request, 'vendor_dashboard.html', {'error': 'No vendor profile found.'})

    # Fetch services associated with the current vendor
    services = Service.objects.filter(vendor=vendor)  # Ensure this is correct
    print(f"Vendor: {vendor}, Services Count: {services.count()}, Services List: {list(services)}")  # Debug print

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.vendor = vendor  # Ensure the vendor is set correctly
            service.save()
            return redirect('vendor_dashboard')
    else:
        form = ServiceForm()

    return render(request, 'vendor_dashboard.html', {
        'form': form,
        'services': services,
        'vendor': vendor,
    })

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def create_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user  # Associate the post with the logged-in user
            blog_post.save()
            return redirect('home')  # Redirect to home or another page after saving
    else:
        form = BlogPostForm()
    
    return render(request, 'create_blog_post.html', {'form': form})

def blog_post_detail(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render(request, 'blog_post_detail.html', {'post': post})

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog_list.html', {'posts': posts})

def blog_detail(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render(request, 'blog_detail.html', {'post': post})


@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            try:
                vendor = Vendor.objects.get(user=request.user)
                service.vendor = vendor
                service.save()
                messages.success(request, "Service added successfully!")
                return redirect('vendor_dashboard')
            except Vendor.DoesNotExist:
                messages.error(request, "Please complete your Vendor profile first.")
                print("Error: Vendor profile not found for current user.")
        else:
            print("Form is invalid. Errors:", form.errors)
            messages.error(request, "There was an error with your submission.")
    else:
        form = ServiceForm()
    
    return render(request, 'add_service.html', {'form': form})

def catering_services(request):
    services = Service.objects.filter(category='Catering')
    return render(request, 'catering_services.html', {'services': services})

# views.py
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'service_detail.html', {'service': service})


