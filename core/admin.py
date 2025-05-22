from django.contrib import admin
from .models import Slider, Category, Product, AboutSection, TeamMember, Testimonial, InstagramSection, InstagramImage, MapLocation

# Register your models here.
admin.site.register(Slider)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(AboutSection)
admin.site.register(TeamMember)
admin.site.register(Testimonial)

class InstagramImageInline(admin.TabularInline):
    model = InstagramImage
    extra = 1

class InstagramSectionAdmin(admin.ModelAdmin):
    inlines = [InstagramImageInline]

admin.site.register(InstagramSection, InstagramSectionAdmin)
admin.site.register(MapLocation)