from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Slider, Category, Product, AboutSection, TeamMember, Testimonial,
    InstagramSection, MapLocation, ContactDetail
)
from .forms import ContactForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

def home(request):
    sliders = Slider.objects.all()
    about = AboutSection.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all()[:8]
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

def shop(request):
    products = Product.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort')

    if category_id:
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(Q(name__icontains=search_query))

    if sort_by == 'a_to_z':
        products = products.order_by('name')
    elif sort_by == 'price_low_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-price')

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': Category.objects.all(),
        'page_obj': page_obj,
        'total_results': products.count(),
    }
    return render(request, 'shop.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })