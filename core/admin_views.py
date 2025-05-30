# project/admin_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Slider, AboutSection, BlogCategory, BlogPost, Testimonial, InstagramSection, InstagramImage
from .admin_forms import (
    AdminSliderForm, AboutSectionForm, BlogCategoryForm, BlogPostForm, TestimonialForm,
    InstagramSectionForm, InstagramImageForm
)
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory

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
def blog_categories_list(request):
    categories = BlogCategory.objects.all()
    return render(request, 'dashboard/blog_categories_list.html', {'categories': categories})

def add_blog_category(request):
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog category added successfully.')
            return redirect('blog_categories_list')
    else:
        form = BlogCategoryForm()
    return render(request, 'dashboard/blog_category_form.html', {'form': form, 'title': 'Add Blog Category'})

@login_required
def edit_blog_category(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog category updated successfully.')
            return redirect('blog_categories_list')
    else:
        form = BlogCategoryForm(instance=category)
    return render(request, 'dashboard/blog_category_form.html', {'form': form, 'title': 'Edit Blog Category'})

@login_required
def delete_blog_category(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Blog category deleted successfully.')
        return redirect('blog_categories_list')
    return render(request, 'dashboard/blog_category_confirm_delete.html', {'category': category})

@login_required
def blog_posts_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'dashboard/blog_posts_list.html', {'posts': posts})

@login_required
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post added successfully.')
            return redirect('blog_posts_list')
    else:
        form = BlogPostForm()
    return render(request, 'dashboard/blog_post_form.html', {'form': form, 'title': 'Add Blog Post'})

@login_required
def edit_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully.')
            return redirect('blog_posts_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'dashboard/blog_post_form.html', {'form': form, 'title': 'Edit Blog Post'})

@login_required
def delete_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('blog_posts_list')
    return render(request, 'dashboard/blog_post_confirm_delete.html', {'post': post})

@login_required
def testimonials_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'dashboard/testimonials_list.html', {'testimonials': testimonials})

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial added successfully.')
            return redirect('testimonials_list')
    else:
        form = TestimonialForm()
    return render(request, 'dashboard/testimonial_form.html', {'form': form, 'title': 'Add Testimonial'})

@login_required
def edit_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully.')
            return redirect('testimonials_list')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'dashboard/testimonial_form.html', {'form': form, 'title': 'Edit Testimonial'})

@login_required
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully.')
        return redirect('testimonials_list')
    return render(request, 'dashboard/testimonial_confirm_delete.html', {'testimonial': testimonial})

InstagramImageFormSet = modelformset_factory(
    InstagramImage,
    form=InstagramImageForm,
    extra=2,          # allow 2 extra blank forms for new images
    can_delete=True
)

@login_required
def instagram_sections_list(request):
    section = InstagramSection.objects.first()
    return render(request, 'dashboard/instagram_sections_list.html', {
        'section': section,
        'images': InstagramImage.objects.filter(section=section) if section else []
    })

@login_required
def edit_instagram_section(request):
    section = get_object_or_404(InstagramSection)

    if request.method == "POST":
        form = InstagramSectionForm(request.POST, instance=section)
        formset = InstagramImageFormSet(request.POST, request.FILES, queryset=InstagramImage.objects.filter(section=section))

        if form.is_valid() and formset.is_valid():
            form.save()

            for img_form in formset:
                if img_form.cleaned_data.get('DELETE') and img_form.instance.pk:
                    img_form.instance.delete()
                elif img_form.cleaned_data.get('image'):
                    image = img_form.save(commit=False)
                    image.section = section
                    image.save()

            messages.success(request, "Instagram section updated successfully.")
            return redirect("instagram_sections_list")
        else:
            print("FORM ERRORS:", form.errors)
            for f in formset:
                print(f.errors)
            messages.error(request, "Please fix the errors below.")
    else:
        form = InstagramSectionForm(instance=section)
        formset = InstagramImageFormSet(queryset=InstagramImage.objects.filter(section=section))

    return render(request, "dashboard/instagram_section_form.html", {
        "form": form,
        "formset": formset,
        "title": "Edit Instagram Section",
    })

@login_required
def add_instagram_section(request):
    if InstagramSection.objects.exists():
        messages.info(request, "Instagram section already exists. You can edit it.")
        return redirect('edit_instagram_section')

    if request.method == 'POST':
        form = InstagramSectionForm(request.POST)
        formset = InstagramImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            section = form.save()
            images = formset.save(commit=False)
            for img in images:
                img.section = section
                img.save()
            formset.save_m2m()
            messages.success(request, "Instagram section added successfully.")
            return redirect('edit_instagram_section')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InstagramSectionForm()
        formset = InstagramImageFormSet()

    return render(request, 'dashboard/instagram_section_form.html', {
        'form': form,
        'formset': formset,
        'edit': False,
        'title': 'Add Instagram Section',
    })

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
def contact_messages_list(request):
    return render(request, 'dashboard/contact_messages_list.html')

@login_required
def map_locations_list(request):
    return render(request, 'dashboard/map_locations_list.html')

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
def newsletter_subscribers_list(request):
    return render(request, 'dashboard/newsletter_subscribers_list.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with your actual homepage url name
