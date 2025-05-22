from django.contrib import admin
from .models import Slider, Category, Product, AboutSection

# Register your models here.
admin.site.register(Slider)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(AboutSection)