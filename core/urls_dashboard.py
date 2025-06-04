from django.urls import path
from . import admin_views

urlpatterns = [
    # Core
    path('', admin_views.dashboard_home, name='dashboard_home'),

    # Sliders
    path('sliders/', admin_views.sliders_list, name='sliders_list'),
    path('sliders/add/', admin_views.add_slider, name='add_slider'),
    path('sliders/edit/<int:pk>/', admin_views.edit_slider, name='edit_slider'),
    path('sliders/delete/<int:pk>/', admin_views.delete_slider, name='delete_slider'),

    # About Section
    path('about/', admin_views.about_section, name='about_section'),
    path('about-section/add/', admin_views.add_about_section, name='add_about_section'),
    path('about-section/edit/<int:pk>/', admin_views.edit_about_section, name='edit_about_section'),

    # Blog Categories
    path('blog-categories/', admin_views.blog_categories_list, name='blog_categories_list'),
    path('blog-categories/add/', admin_views.add_blog_category, name='add_blog_category'),
    path('blog-categories/edit/<int:pk>/', admin_views.edit_blog_category, name='edit_blog_category'),
    path('blog-categories/delete/<int:pk>/', admin_views.delete_blog_category, name='delete_blog_category'),

    # Blog Posts
    path('blog-posts/', admin_views.blog_posts_list, name='blog_posts_list'),
    path('blog-posts/add/', admin_views.add_blog_post, name='add_blog_post'),
    path('blog-posts/edit/<int:pk>/', admin_views.edit_blog_post, name='edit_blog_post'),
    path('blog-posts/delete/<int:pk>/', admin_views.delete_blog_post, name='delete_blog_post'),

    # Testimonials
    path('testimonials/', admin_views.testimonials_list, name='testimonials_list'),
    path('testimonials/add/', admin_views.add_testimonial, name='add_testimonial'),
    path('testimonials/edit/<int:pk>/', admin_views.edit_testimonial, name='edit_testimonial'),
    path('testimonials/delete/<int:pk>/', admin_views.delete_testimonial, name='delete_testimonial'),

    # Instagram Sections
    path('instagram-sections/', admin_views.instagram_sections_list, name='instagram_sections_list'),
    path('instagram-sections/add/', admin_views.add_instagram_section, name='add_instagram_section'),
    path('instagram-sections/edit/', admin_views.edit_instagram_section, name='edit_instagram_section'),

    # Categories
    path('categories/', admin_views.category_list, name='category_list'),
    path('categories/add/', admin_views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', admin_views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', admin_views.delete_category, name='delete_category'),

    # Products
    path('products/', admin_views.product_list, name='product_list'),
    path('products/add/', admin_views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', admin_views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', admin_views.delete_product, name='delete_product'),

    # Coupons
    path('coupons/', admin_views.coupons_list, name='coupons_list'),
    path('coupons/add/', admin_views.add_coupon, name='add_coupon'),
    path('coupons/edit/<int:pk>/', admin_views.edit_coupon, name='edit_coupon'),
    path('coupons/delete/<int:pk>/', admin_views.delete_coupon, name='delete_coupon'),

    # Users
    path('users/', admin_views.users_list, name='users_list'),
    path('users/add/', admin_views.add_user, name='add_user'),
    path('users/edit/<int:pk>/', admin_views.edit_user, name='edit_user'),
    path('users/delete/<int:pk>/', admin_views.delete_user, name='delete_user'),

    # User Profiles
    path('userprofiles/', admin_views.userprofiles_list, name='userprofiles_list'),
    path('userprofiles/edit/<int:pk>/', admin_views.edit_userprofile, name='edit_userprofile'),

    # Wishlist Items
    path('wishlist-items/', admin_views.wishlist_items_list, name='wishlist_items_list'),
    path('wishlist-items/delete/<int:pk>/', admin_views.delete_wishlist_item, name='delete_wishlist_item'),

    # Orders
    path('orders/', admin_views.order_list, name='admin_order_list'),
    path('orders/<int:pk>/', admin_views.order_detail, name='admin_order_detail'),
    path('orders/delete/<int:pk>/', admin_views.order_delete, name='admin_order_delete'),

    # Team Members
    path('team-members/', admin_views.team_members_list, name='team_members_list'),
    path('team-members/add/', admin_views.add_team_member, name='add_team_member'),
    path('team-members/edit/<int:pk>/', admin_views.edit_team_member, name='edit_team_member'),
    path('team-members/delete/<int:pk>/', admin_views.delete_team_member, name='delete_team_member'),

    # Map Location
    path('map-location/', admin_views.maplocation_list, name='maplocation_list'),
    path('map-location/add/', admin_views.maplocation_edit, name='maplocation_add'),
    path('map-location/edit/<int:pk>/', admin_views.maplocation_edit, name='maplocation_edit'),

    # Contact Detail
    path('contact-detail/', admin_views.contactdetail_list, name='contactdetail_list'),
    path('contact-detail/add/', admin_views.contactdetail_edit, name='contactdetail_add'),
    path('contact-detail/edit/<int:pk>/', admin_views.contactdetail_edit, name='contactdetail_edit'),

    # Contact Messages
    path('dashboard/contact-messages/', admin_views.contact_messages_list, name='contact_messages_list'),
    path('dashboard/contact-messages/delete/<int:pk>/', admin_views.contact_message_delete, name='contact_message_delete'),

    # Newsletter Subscribers
    path('newsletter-subscribers/', admin_views.newsletter_subscribers_list, name='newsletter_subscribers_list'),
    path('newsletter-subscribers/delete/<int:pk>/', admin_views.delete_newsletter_subscriber, name='delete_newsletter_subscriber'),

    # Special Offers
    path('specialoffers/', admin_views.specialoffers_list, name='specialoffers_list'),
    path('specialoffers/add/', admin_views.add_specialoffer, name='specialoffer_add'),
    path('specialoffers/edit/<int:pk>/', admin_views.edit_specialoffer, name='specialoffer_edit'),
    path('specialoffers/delete/<int:pk>/', admin_views.delete_specialoffer, name='specialoffer_delete'),

    # Organization Details (Singleton)
    path('organizationdetails/add/', admin_views.add_organization_details, name='add_organization_details'),
    path('organizationdetails/edit/', admin_views.edit_organization_details, name='edit_organization_details'),
    path('organizationdetails/', admin_views.organization_details, name='organization_details_list')
]
