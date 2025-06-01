from django.urls import path
from . import views

urlpatterns = [
    # Core pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Shop & Product
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
    path('register/', views.register_user, name='register'),

    # User Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),

    # Newsletter
    path('newsletter-signup/', views.newsletter_signup_ajax, name='newsletter_signup_ajax'),

    # Search
    path('search/', views.search_results, name='search_results'),
]
