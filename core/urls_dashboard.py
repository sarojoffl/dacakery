# project/urls_dashboard.py
from django.urls import path
from . import admin_views

urlpatterns = [
    # Core
    path('', admin_views.dashboard_home, name='dashboard_home'),

    # Manage
    path('sliders/', admin_views.sliders_list, name='sliders_list'),
    path('about/', admin_views.about_section, name='about_section'),
    path('categories/', admin_views.categories_list, name='categories_list'),
    path('products/', admin_views.products_list, name='products_list'),
    path('team-members/', admin_views.team_members_list, name='team_members_list'),
    path('testimonials/', admin_views.testimonials_list, name='testimonials_list'),
    path('instagram-sections/', admin_views.instagram_sections_list, name='instagram_sections_list'),
    path('instagram-images/', admin_views.instagram_images_list, name='instagram_images_list'),
    path('map-locations/', admin_views.map_locations_list, name='map_locations_list'),
    path('contact-details/', admin_views.contact_details_list, name='contact_details_list'),
    path('contact-messages/', admin_views.contact_messages_list, name='contact_messages_list'),
    path('users/', admin_views.users_list, name='users_list'),
    path('wishlist-items/', admin_views.wishlist_items_list, name='wishlist_items_list'),
    path('orders/', admin_views.orders_list, name='orders_list'),
    path('order-items/', admin_views.order_items_list, name='order_items_list'),
    path('coupons/', admin_views.coupons_list, name='coupons_list'),
    path('blog-categories/', admin_views.blog_categories_list, name='blog_categories_list'),
    path('blog-posts/', admin_views.blog_posts_list, name='blog_posts_list'),
    path('newsletter-subscribers/', admin_views.newsletter_subscribers_list, name='newsletter_subscribers_list'),
]
