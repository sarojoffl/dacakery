# project/admin_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html')

@login_required
def sliders_list(request):
    return render(request, 'dashboard/sliders_list.html')

@login_required
def categories_list(request):
    return render(request, 'dashboard/categories_list.html')

@login_required
def products_list(request):
    return render(request, 'dashboard/products_list.html')

@login_required
def team_members_list(request):
    return render(request, 'dashboard/team_members_list.html')

@login_required
def testimonials_list(request):
    return render(request, 'dashboard/testimonials_list.html')

@login_required
def about_section(request):
    return render(request, 'dashboard/about_section.html')

@login_required
def blog_posts_list(request):
    return render(request, 'dashboard/blog_posts_list.html')

@login_required
def contact_messages_list(request):
    return render(request, 'dashboard/contact_messages_list.html')

@login_required
def map_locations_list(request):
    return render(request, 'dashboard/map_locations_list.html')

@login_required
def instagram_sections_list(request):
    return render(request, 'dashboard/instagram_sections_list.html')

@login_required
def instagram_images_list(request):
    return render(request, 'dashboard/instagram_images_list.html')

@login_required
def contact_details_list(request):
    return render(request, 'dashboard/contact_details_list.html')

@login_required
def users_list(request):
    return render(request, 'dashboard/users_list.html')

@login_required
def wishlist_items_list(request):
    return render(request, 'dashboard/wishlist_items_list.html')

@login_required
def orders_list(request):
    return render(request, 'dashboard/orders_list.html')

@login_required
def order_items_list(request):
    return render(request, 'dashboard/order_items_list.html')

@login_required
def coupons_list(request):
    return render(request, 'dashboard/coupons_list.html')

@login_required
def blog_categories_list(request):
    return render(request, 'dashboard/blog_categories_list.html')

@login_required
def newsletter_subscribers_list(request):
    return render(request, 'dashboard/newsletter_subscribers_list.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with your actual homepage url name
