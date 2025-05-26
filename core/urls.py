from django.urls import path
from . import views
from django.http import HttpResponse

# Placeholder for pages not yet implemented
def placeholder_view(request):
    return HttpResponse("This page is coming soon.")

urlpatterns = [
    # Core pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Shop & product
    path('shop/', views.shop, name='shop'),
    path('shop/<slug:slug>/', views.product_detail, name='product_detail'),

    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Coupons
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),

    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', placeholder_view, name='register'),

    # Profile
    path('profile/', views.profile, name='profile'),

    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
]
