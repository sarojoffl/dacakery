# project/admin_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Slider, AboutSection
from .admin_forms import AdminSliderForm, AboutSectionForm
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html')

@login_required
def sliders_list(request):
    sliders = Slider.objects.all()
    return render(request, 'dashboard/sliders_list.html', {'sliders': sliders})

@login_required
def add_slider(request):
    if request.method == 'POST':
        form = AdminSliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider added successfully.')
            return redirect('sliders_list')
    else:
        form = AdminSliderForm()
    return render(request, 'dashboard/slider_form.html', {'form': form, 'title': 'Add Slider'})

@login_required
def edit_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        form = AdminSliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider updated successfully.')
            return redirect('sliders_list')
    else:
        form = AdminSliderForm(instance=slider)
    return render(request, 'dashboard/slider_form.html', {'form': form, 'title': 'Edit Slider'})

@login_required
def delete_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        slider.delete()
        messages.success(request, 'Slider deleted successfully.')
        return redirect('sliders_list')
    return render(request, 'dashboard/slider_confirm_delete.html', {'slider': slider})

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
    about = AboutSection.objects.first()
    return render(request, 'dashboard/about_section.html', {'about': about})

@login_required
def add_about_section(request):
    if request.method == 'POST':
        form = AboutSectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "About section created successfully.")
            return redirect('about_section')
    else:
        form = AboutSectionForm()
    return render(request, 'dashboard/about_section_form.html', {'form': form, 'title': 'Add About Section'})

@login_required
def edit_about_section(request, pk):
    about = get_object_or_404(AboutSection, pk=pk)
    if request.method == 'POST':
        form = AboutSectionForm(request.POST, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, "About section updated successfully.")
            return redirect('about_section')
    else:
        form = AboutSectionForm(instance=about)
    return render(request, 'dashboard/about_section_form.html', {'form': form, 'title': 'Edit About Section'})

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
