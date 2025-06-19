# project/admin_views.py
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import modelformset_factory

from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum

import csv
import json

def staff_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/login/'  # or reverse('login')
    )(view_func)
    return decorated_view_func

from .models import (
    Slider, AboutSection, BlogCategory, BlogPost, Testimonial, InstagramSection,
    InstagramImage, Category, Product, ProductImage, Coupon, WishlistItem, Order, NewsletterSubscriber,
    TeamMember, MapLocation, ContactDetail, ContactMessage, FlashSale, OrganizationDetails, UserProfile,
    ProductOption, ProductOptionPrice, FlashSaleItem
)

from .admin_forms import (
    AdminSliderForm, AboutSectionForm, BlogCategoryForm, BlogPostForm, TestimonialForm,
    InstagramSectionForm, InstagramImageForm, CategoryForm, ProductForm, ProductImageForm, CouponForm, UserForm, TeamMemberForm,
    MapLocationForm, ContactDetailForm, FlashSaleForm, OrganizationDetailsForm, UserProfileForm, AdminOrderForm,
    ProductOptionForm, ProductOptionPriceForm, FlashSaleItemForm
)

# -- -------- Dashboard Home ---------
@staff_required
def dashboard_home(request):
    sales_data = (
        Order.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(order_count=Count('id'))
        .order_by('month')
    )

    revenue_data = (
        Order.objects
        .filter(status='paid')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total_amount'))
        .order_by('month')
    )

    labels = [entry['month'] for entry in sales_data]

    revenue_map = {entry['month']: float(entry['revenue'] or 0) for entry in revenue_data}  # Convert Decimal to float

    chart_labels = [month.strftime('%b %Y') for month in labels]

    sales = [entry['order_count'] for entry in sales_data]

    revenue = [revenue_map.get(month, 0) for month in labels]

    context = {
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'total_products': Product.objects.count(),
        'total_messages': ContactMessage.objects.count(),
        'chart_labels': json.dumps(chart_labels),  # <-- dump to JSON string
        'chart_data': json.dumps(sales),           # <-- dump to JSON string
        'revenue_data': json.dumps(revenue),       # <-- dump to JSON string
    }
    return render(request, 'dashboard/home.html', context)

# -- -------- Sliders ---------
@staff_required
def sliders_list(request):
    sliders = Slider.objects.all()
    return render(request, 'dashboard/sliders_list.html', {'sliders': sliders})

@staff_required
def add_slider(request):
    if Slider.objects.count() >= 2:
        messages.warning(request, "You can only add up to 2 sliders.")
        return redirect('sliders_list')

    if request.method == 'POST':
        form = AdminSliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider added successfully.')
            return redirect('sliders_list')
    else:
        form = AdminSliderForm()
    return render(request, 'dashboard/slider_form.html', {'form': form, 'title': 'Add Slider'})

@staff_required
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

@staff_required
def delete_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        slider.delete()
        messages.success(request, 'Slider deleted successfully.')
        return redirect('sliders_list')
    return render(request, 'dashboard/slider_confirm_delete.html', {'slider': slider})

# -- -------- About Section ---------
@staff_required
def about_section(request):
    about = AboutSection.objects.first()
    return render(request, 'dashboard/about_section.html', {'about': about})

@staff_required
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

@staff_required
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

# -- -------- Blog Categories ---------
@staff_required
def blog_categories_list(request):
    categories = BlogCategory.objects.all()
    return render(request, 'dashboard/blog_categories_list.html', {'categories': categories})

@staff_required
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

@staff_required
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

@staff_required
def delete_blog_category(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Blog category deleted successfully.')
        return redirect('blog_categories_list')
    return render(request, 'dashboard/blog_category_confirm_delete.html', {'category': category})

# -- -------- Blog Posts ---------
@staff_required
def blog_posts_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'dashboard/blog_posts_list.html', {'posts': posts})

@staff_required
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

@staff_required
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

@staff_required
def delete_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('blog_posts_list')
    return render(request, 'dashboard/blog_post_confirm_delete.html', {'post': post})

# -- -------- Testimonials ---------
@staff_required
def testimonials_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'dashboard/testimonials_list.html', {'testimonials': testimonials})

@staff_required
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

@staff_required
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

@staff_required
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully.')
        return redirect('testimonials_list')
    return render(request, 'dashboard/testimonial_confirm_delete.html', {'testimonial': testimonial})

# -- -------- Instagram Sections ---------
InstagramImageFormSet = modelformset_factory(
    InstagramImage,
    form=InstagramImageForm,
    extra=2,          # allow 2 extra blank forms for new images
    can_delete=True
)

@staff_required
def instagram_sections_list(request):
    section = InstagramSection.objects.first()
    return render(request, 'dashboard/instagram_sections_list.html', {
        'section': section,
        'images': InstagramImage.objects.filter(section=section) if section else []
    })

@staff_required
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

@staff_required
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

# -- -------- Categories ---------
@staff_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})


@staff_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Add Category'})


@staff_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Edit Category'})


@staff_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})

# -- -------- Products ---------
ProductImageFormSet = modelformset_factory(
    ProductImage,
    form=ProductImageForm,
    extra=2,           # can be more
    can_delete=True
)

@staff_required
def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'dashboard/product_list.html', {'products': products})


@staff_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())

        if form.is_valid() and formset.is_valid():
            product = form.save()

            for image_form in formset:
                if image_form.cleaned_data.get('image'):
                    image = image_form.save(commit=False)
                    image.product = product
                    image.save()

            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
        formset = ProductImageFormSet(queryset=ProductImage.objects.none())

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Add Product'
    })


@staff_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.filter(product=product))

        if form.is_valid() and formset.is_valid():
            form.save()

            for image_form in formset:
                if image_form.cleaned_data.get('DELETE') and image_form.instance.pk:
                    image_form.instance.delete()
                elif image_form.cleaned_data.get('image'):
                    image = image_form.save(commit=False)
                    image.product = product
                    image.save()

            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(queryset=ProductImage.objects.filter(product=product))

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Edit Product',
        'product': product
    })


@staff_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})

# ----- ProductOption Views -----

@staff_required
def product_option_list(request):
    options = ProductOption.objects.all()
    return render(request, 'dashboard/product_option_list.html', {'options': options})

@staff_required
def product_option_create(request):
    form = ProductOptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Product option created successfully!")
        return redirect('product_option_list')
    return render(request, 'dashboard/product_option_form.html', {'form': form, 'title': 'Add Product Option'})

@staff_required
def product_option_update(request, pk):
    option = get_object_or_404(ProductOption, pk=pk)
    form = ProductOptionForm(request.POST or None, instance=option)
    if form.is_valid():
        form.save()
        messages.success(request, "Product option updated successfully!")
        return redirect('product_option_list')
    return render(request, 'dashboard/product_option_form.html', {'form': form, 'title': 'Edit Product Option'})

@staff_required
def product_option_delete(request, pk):
    option = get_object_or_404(ProductOption, pk=pk)
    if request.method == 'POST':
        option.delete()
        messages.success(request, "Product option deleted.")
        return redirect('product_option_list')
    return render(request, 'dashboard/delete_confirm.html', {'object': option, 'cancel_url': 'product_option_list'})


# ----- ProductOptionPrice Views -----

@staff_required
def product_option_price_list(request):
    prices = ProductOptionPrice.objects.select_related('product', 'option')
    return render(request, 'dashboard/product_option_price_list.html', {'prices': prices})

@staff_required
def product_option_price_create(request):
    form = ProductOptionPriceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Product option price created!")
        return redirect('product_option_price_list')
    return render(request, 'dashboard/product_option_price_form.html', {'form': form, 'title': 'Add Option Price'})

@staff_required
def product_option_price_update(request, pk):
    price = get_object_or_404(ProductOptionPrice, pk=pk)
    form = ProductOptionPriceForm(request.POST or None, instance=price)
    if form.is_valid():
        form.save()
        messages.success(request, "Product option price updated!")
        return redirect('product_option_price_list')
    return render(request, 'dashboard/product_option_price_form.html', {'form': form, 'title': 'Edit Option Price'})

@staff_required
def product_option_price_delete(request, pk):
    price = get_object_or_404(ProductOptionPrice, pk=pk)
    if request.method == 'POST':
        price.delete()
        messages.success(request, "Product option price deleted.")
        return redirect('product_option_price_list')
    return render(request, 'dashboard/delete_confirm.html', {'object': price, 'cancel_url': 'product_option_price_list'})

# -- -------- Coupons ---------
@staff_required
def coupons_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'dashboard/coupons_list.html', {'coupons': coupons})

@staff_required
def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon added successfully.')
            return redirect('coupons_list')
    else:
        form = CouponForm()
    return render(request, 'dashboard/coupon_form.html', {'form': form, 'title': 'Add Coupon'})

@staff_required
def edit_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon updated successfully.')
            return redirect('coupons_list')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'dashboard/coupon_form.html', {'form': form, 'title': 'Edit Coupon'})

@staff_required
def delete_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        messages.success(request, 'Coupon deleted successfully.')
        return redirect('coupons_list')
    return render(request, 'dashboard/coupon_confirm_delete.html', {'coupon': coupon})

# -- -------- Users ---------
@staff_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/users_list.html', {'users': users})

@staff_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('users_list')
    else:
        form = UserForm()
    return render(request, 'dashboard/user_form.html', {'form': form, 'title': 'Add User'})

@staff_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('users_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'dashboard/user_form.html', {'form': form, 'title': 'Edit User'})

@staff_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if user.is_superuser:
        messages.error(request, "You cannot delete a superuser.")
        return redirect('users_list')
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('users_list')
    
    return render(request, 'dashboard/user_confirm_delete.html', {'user': user})

# -- -------- User Profiles ---------
@staff_required
def userprofiles_list(request):
    profiles = UserProfile.objects.select_related('user').all()
    return render(request, 'dashboard/userprofiles_list.html', {'profiles': profiles})

@staff_required
def edit_userprofile(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    social_fields = ['facebook', 'instagram', 'twitter', 'linkedin']

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile updated successfully.')
            return redirect('userprofiles_list')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'title': 'Edit User Profile',
        'social_fields': social_fields,
    }
    return render(request, 'dashboard/userprofile_form.html', context)

# -- -------- Wishlist Items ---------
@staff_required
def wishlist_items_list(request):
    items = WishlistItem.objects.select_related('user', 'product').all()
    return render(request, 'dashboard/wishlist_items_list.html', {'items': items})

@staff_required
def delete_wishlist_item(request, pk):
    item = get_object_or_404(WishlistItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Wishlist item deleted successfully.')
        return redirect('wishlist_items_list')
    return render(request, 'dashboard/wishlist_item_confirm_delete.html', {'item': item})

# -- -------- Orders ---------
@staff_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@staff_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'dashboard/order_detail.html', {'order': order})

@staff_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = AdminOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully.')
            return redirect('admin_order_detail', pk=order.pk)
    else:
        form = AdminOrderForm(instance=order)
    return render(request, 'dashboard/order_form.html', {'form': form, 'title': 'Edit Order'})

@staff_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully.')
        return redirect('admin_order_list')
    return render(request, 'dashboard/order_confirm_delete.html', {'order': order})

# -- -------- Team Members ---------
@staff_required
def team_members_list(request):
    members = TeamMember.objects.all()
    return render(request, 'dashboard/team_members_list.html', {'members': members})

@staff_required
def add_team_member(request):
    form = TeamMemberForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Team member added successfully.")
        return redirect('team_members_list')
    return render(request, 'dashboard/team_member_form.html', {'form': form, 'title': 'Add Team Member'})

@staff_required
def edit_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    form = TeamMemberForm(request.POST or None, request.FILES or None, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, "Team member updated successfully.")
        return redirect('team_members_list')
    return render(request, 'dashboard/team_member_form.html', {'form': form, 'title': 'Edit Team Member'})

@staff_required
def delete_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Team member deleted successfully.")
        return redirect('team_members_list')
    return render(request, 'dashboard/team_member_confirm_delete.html', {'member': member})

# -- -------- Map Location (Singleton) ---------
@staff_required
def maplocation_list(request):
    map_location = MapLocation.objects.first()
    return render(request, 'dashboard/maplocation_list.html', {'map_location': map_location, 'title': 'Map Location'})

@staff_required
def maplocation_edit(request, pk=None):
    instance = None
    if pk:
        instance = get_object_or_404(MapLocation, pk=pk)
    else:
        instance = MapLocation.objects.first()

    if request.method == 'POST':
        form = MapLocationForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Map Location saved successfully.")
            return redirect('maplocation_list')
    else:
        form = MapLocationForm(instance=instance)

    return render(request, 'dashboard/maplocation_form.html', {'form': form, 'title': 'Edit Map Location' if instance else 'Add Map Location'})

# -- -------- Contact Detail (Singleton) ---------
@staff_required
def contactdetail_list(request):
    contact_detail = ContactDetail.objects.first()
    return render(request, 'dashboard/contactdetail_list.html', {'contact_detail': contact_detail, 'title': 'Contact Detail'})

@staff_required
def contactdetail_edit(request, pk=None):
    instance = None
    if pk:
        instance = get_object_or_404(ContactDetail, pk=pk)
    else:
        instance = ContactDetail.objects.first()

    if request.method == 'POST':
        form = ContactDetailForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact Detail saved successfully.")
            return redirect('contactdetail_list')
    else:
        form = ContactDetailForm(instance=instance)

    return render(request, 'dashboard/contactdetail_form.html', {'form': form, 'title': 'Edit Contact Detail' if instance else 'Add Contact Detail'})

# -- -------- Contact Messages ---------
@staff_required
def contact_messages_list(request):
    messages_list = ContactMessage.objects.order_by('-submitted_at')
    return render(request, 'dashboard/contact_messages_list.html', {
        'messages_list': messages_list,
        'title': 'Contact Messages'
    })

@staff_required
def contact_message_delete(request, pk):
    message_obj = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        message_obj.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect('contact_messages_list')
    return render(request, 'dashboard/contact_message_confirm_delete.html', {
        'message': message_obj,
        'title': 'Delete Contact Message'
    })

# ---------- Newsletter Subscribers ---------
@staff_required
def newsletter_subscribers_list(request):
    subscribers = NewsletterSubscriber.objects.all()
    return render(request, 'dashboard/newsletter_subscribers_list.html', {'subscribers': subscribers})

@staff_required
def delete_newsletter_subscriber(request, pk):
    subscriber = get_object_or_404(NewsletterSubscriber, pk=pk)
    if request.method == 'POST':
        subscriber.delete()
        messages.success(request, '🗑️ Newsletter subscriber deleted successfully.')
        return redirect('newsletter_subscribers_list')
    return render(request, 'dashboard/newsletter_subscribers_confirm_delete.html', {
        'subscriber': subscriber
    })

@staff_required
def export_newsletter_subscribers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="newsletter_subscribers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Email', 'Subscribed At'])

    for sub in NewsletterSubscriber.objects.all():
        writer.writerow([sub.email, sub.subscribed_at])

    return response

# -------- Logout View ---------
@staff_required
def logout_view(request):
    logout(request)
    return redirect('home')

# -------- Flash Sales ---------
@staff_required
def flashsales_list(request):
    flashsales = FlashSale.objects.all()
    return render(request, 'dashboard/flashsales_list.html', {'flashsales': flashsales})

@staff_required
def add_flashsale(request):
    if request.method == 'POST':
        form = FlashSaleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Flash Sale added successfully!")
            return redirect('flashsales_list')
    else:
        form = FlashSaleForm()
    return render(request, 'dashboard/flashsale_form.html', {'form': form, 'title': 'Add Flash Sale'})

@staff_required
def edit_flashsale(request, pk):
    flashsale = get_object_or_404(FlashSale, pk=pk)
    if request.method == 'POST':
        form = FlashSaleForm(request.POST, request.FILES, instance=flashsale)
        if form.is_valid():
            form.save()
            messages.success(request, "Flash Sale updated successfully!")
            return redirect('flashsales_list')
    else:
        form = FlashSaleForm(instance=flashsale)
    return render(request, 'dashboard/flashsale_form.html', {'form': form, 'title': 'Edit Flash Sale'})

@staff_required
def delete_flashsale(request, pk):
    flashsale = get_object_or_404(FlashSale, pk=pk)
    if request.method == 'POST':
        flashsale.delete()
        messages.success(request, "Flash Sale deleted successfully!")
        return redirect('flashsales_list')
    return render(request, 'dashboard/flashsale_confirm_delete.html', {
        'flashsale': flashsale,
        'title': 'Delete Flash Sale'
    })

# -------- Flash Sale Items ---------
@staff_required
def admin_flashsaleitem_list(request):
    items = FlashSaleItem.objects.select_related('flash_sale', 'product').all()
    context = {'items': items}
    return render(request, 'dashboard/flashsaleitem_list.html', context)

@staff_required
def admin_flashsaleitem_add(request):
    if request.method == 'POST':
        form = FlashSaleItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Flash sale item added successfully!')
            return redirect('flashsaleitem_list')
    else:
        form = FlashSaleItemForm()
    return render(request, 'dashboard/flashsaleitem_form.html', {'form': form})

@staff_required
def admin_flashsaleitem_edit(request, pk):
    item = get_object_or_404(FlashSaleItem, pk=pk)
    if request.method == 'POST':
        form = FlashSaleItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Flash sale item updated successfully!')
            return redirect('flashsaleitem_list')
    else:
        form = FlashSaleItemForm(instance=item)
    return render(request, 'dashboard/flashsaleitem_form.html', {'form': form, 'item': item})

@staff_required
def admin_flashsaleitem_delete(request, pk):
    item = get_object_or_404(FlashSaleItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Flash sale item deleted successfully! 🗑️')
        return redirect('flashsaleitem_list')
    return render(request, 'dashboard/flashsaleitem_confirm_delete.html', {'item': item})

# -------- Organization Details (Singleton) ---------
@staff_required
def organization_details(request):
    organization = OrganizationDetails.objects.first()
    return render(request, 'dashboard/organizationdetails_detail.html', {'organization': organization})

@staff_required
def add_organization_details(request):
    if OrganizationDetails.objects.exists():
        messages.warning(request, "Organization Details already exist. You can edit them instead.")
        return redirect('edit_organization_details')

    if request.method == 'POST':
        form = OrganizationDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization Details added successfully!")
            return redirect('organization_details_list')
    else:
        form = OrganizationDetailsForm()
    return render(request, 'dashboard/organizationdetails_form.html', {'form': form, 'title': 'Add Organization Details'})

@staff_required
def edit_organization_details(request):
    organizationdetails = OrganizationDetails.objects.first()
    if not organizationdetails:
        messages.warning(request, "No Organization Details found. Please add one first.")
        return redirect('add_organization_details')

    if request.method == 'POST':
        form = OrganizationDetailsForm(request.POST, request.FILES, instance=organizationdetails)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization Details updated successfully!")
            return redirect('organization_details_list')
    else:
        form = OrganizationDetailsForm(instance=organizationdetails)
    return render(request, 'dashboard/organizationdetails_form.html', {'form': form, 'title': 'Edit Organization Details'})