from django.shortcuts import render
from .models import Slider, Category, Product, AboutSection

def home(request):
    sliders = Slider.objects.all()
    about = AboutSection.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'home.html', {
        'sliders': sliders,
        'about': about,
        'categories': categories,
        'products': products,
    })