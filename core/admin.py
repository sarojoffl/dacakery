from django.contrib import admin
from .models import (
    Slider, Category, Product, AboutSection, TeamMember, Testimonial,
    InstagramSection, InstagramImage, MapLocation, ContactDetail, ContactMessage,
    WishlistItem, Order, OrderItem, Coupon
)

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
admin.site.register(ContactDetail)
admin.site.register(ContactMessage)
admin.site.register(WishlistItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'created_at')  # removed 'status'
    list_filter = ()  # removed 'status'
    search_fields = ('user__username', 'id')

admin.site.register(Order, OrderAdmin)


admin.site.register(Coupon)