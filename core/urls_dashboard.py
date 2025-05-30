# project/urls_dashboard.py
from django.urls import path
from . import admin_views

urlpatterns = [
    # Core
    path('', admin_views.dashboard_home, name='dashboard_home'),

    # Manage
    path('sliders/', admin_views.sliders_list, name='sliders_list'),
    path('sliders/add/', admin_views.add_slider, name='add_slider'),
    path('sliders/edit/<int:pk>/', admin_views.edit_slider, name='edit_slider'),
    path('sliders/delete/<int:pk>/', admin_views.delete_slider, name='delete_slider'),


    path('about/', admin_views.about_section, name='about_section'),
    path('about-section/add/', admin_views.add_about_section, name='add_about_section'),
    path('about-section/edit/<int:pk>/', admin_views.edit_about_section, name='edit_about_section'),

    path('blog-categories/', admin_views.blog_categories_list, name='blog_categories_list'),
    path('blog-categories/add/', admin_views.add_blog_category, name='add_blog_category'),
    path('blog-categories/edit/<int:pk>/', admin_views.edit_blog_category, name='edit_blog_category'),
    path('blog-categories/delete/<int:pk>/', admin_views.delete_blog_category, name='delete_blog_category'),

    
    path('blog-posts/', admin_views.blog_posts_list, name='blog_posts_list'),
    path('blog-posts/add/', admin_views.add_blog_post, name='add_blog_post'),
    path('blog-posts/edit/<int:pk>/', admin_views.edit_blog_post, name='edit_blog_post'),
    path('blog-posts/delete/<int:pk>/', admin_views.delete_blog_post, name='delete_blog_post'),
    
    path('testimonials/', admin_views.testimonials_list, name='testimonials_list'),
    path('testimonials/add/', admin_views.add_testimonial, name='add_testimonial'),
    path('testimonials/edit/<int:pk>/', admin_views.edit_testimonial, name='edit_testimonial'),
    path('testimonials/delete/<int:pk>/', admin_views.delete_testimonial, name='delete_testimonial'),

    path('instagram-sections/', admin_views.instagram_sections_list, name='instagram_sections_list'),
    path('nstagram-sections/add/', admin_views.add_instagram_section, name='add_instagram_section'),
    path('instagram-sections/edit/', admin_views.edit_instagram_section, name='edit_instagram_section'),
    
    path('categories/', admin_views.category_list, name='category_list'),
    path('categories/add/', admin_views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', admin_views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', admin_views.delete_category, name='delete_category'),

    path('products/', admin_views.product_list, name='product_list'),
    path('products/add/', admin_views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', admin_views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', admin_views.delete_product, name='delete_product'),

    path('coupons/', admin_views.coupons_list, name='coupons_list'),
    path('coupons/add/', admin_views.add_coupon, name='add_coupon'),
    path('coupons/edit/<int:pk>/', admin_views.edit_coupon, name='edit_coupon'),
    path('coupons/delete/<int:pk>/', admin_views.delete_coupon, name='delete_coupon'),

    path('users/', admin_views.users_list, name='users_list'),
    path('users/add/', admin_views.add_user, name='add_user'),
    path('users/edit/<int:pk>/', admin_views.edit_user, name='edit_user'),
    path('users/delete/<int:pk>/', admin_views.delete_user, name='delete_user'),

    path('wishlist-items/', admin_views.wishlist_items_list, name='wishlist_items_list'),
    path('wishlist-items/delete/<int:pk>/', admin_views.delete_wishlist_item, name='delete_wishlist_item'),


    path('orders/', admin_views.order_list, name='order_list'),
    path('orders/<int:pk>/', admin_views.order_detail, name='order_detail'),
    path('orders/delete/<int:pk>/', admin_views.order_delete, name='order_delete'),

    path('team-members/', admin_views.team_members_list, name='team_members_list'),
    path('team-members/add/', admin_views.add_team_member, name='add_team_member'),
    path('team-members/edit/<int:pk>/', admin_views.edit_team_member, name='edit_team_member'),
    path('team-members/delete/<int:pk>/', admin_views.delete_team_member, name='delete_team_member'),

    path('map-locations/', admin_views.map_locations_list, name='map_locations_list'),
    path('contact-details/', admin_views.contact_details_list, name='contact_details_list'),
    path('contact-messages/', admin_views.contact_messages_list, name='contact_messages_list'),
    
    path('newsletter-subscribers/', admin_views.newsletter_subscribers_list, name='newsletter_subscribers_list'),
    path('newsletter-subscribers/<int:pk>/delete/', admin_views.delete_newsletter_subscriber, name='delete_newsletter_subscriber'),
]
