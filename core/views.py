from django.shortcuts import render, redirect
from .models import (
    Slider, Category, Product, AboutSection, TeamMember, Testimonial,
    InstagramSection, MapLocation, ContactDetail
)
from .forms import ContactForm
from django.views.decorators.http import require_POST
from django.contrib import messages

def home(request):
    sliders = Slider.objects.all()
    about = AboutSection.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all()
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    instagram_section = InstagramSection.objects.prefetch_related('images').first()
    map_location = MapLocation.objects.first()
    return render(request, 'home.html', {
        'sliders': sliders,
        'about': about,
        'categories': categories,
        'products': products,
        'team_members': team_members,
        'testimonials': testimonials,
        'instagram_section': instagram_section,
        'map_location': map_location,
    })

def about(request):
    about = AboutSection.objects.first()
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request, 'about.html', {
        'about': about,
        'team_members': team_members,
        'testimonials': testimonials,
    })

def contact(request):
    contact_detail = ContactDetail.objects.first()
    map_location = MapLocation.objects.first()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'map_location': map_location,
        'contact_detail': contact_detail,
        'form': form,
    })
