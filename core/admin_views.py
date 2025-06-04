# project/admin_views.py
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import (
    Slider, AboutSection, BlogCategory, BlogPost, Testimonial, InstagramSection,
    InstagramImage, Category, Product, Coupon, WishlistItem, Order, NewsletterSubscriber,
    TeamMember, MapLocation, ContactDetail, ContactMessage, SpecialOffer, OrganizationDetails
)
from .admin_forms import (
    AdminSliderForm, AboutSectionForm, BlogCategoryForm, BlogPostForm, TestimonialForm,
    InstagramSectionForm, InstagramImageForm, CategoryForm, ProductForm, CouponForm, UserForm, TeamMemberForm,
    MapLocationForm, ContactDetailForm, SpecialOfferForm, OrganizationDetailsForm
)
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory

# -- -------- Dashboard Home ---------
@staff_member_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html')

# -- -------- Sliders ---------
@staff_member_required
def sliders_list(request):
    sliders = Slider.objects.all()
    return render(request, 'dashboard/sliders_list.html', {'sliders': sliders})

@staff_member_required
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

@staff_member_required
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

@staff_member_required
def delete_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        slider.delete()
        messages.success(request, 'Slider deleted successfully.')
        return redirect('sliders_list')
    return render(request, 'dashboard/slider_confirm_delete.html', {'slider': slider})

# -- -------- About Section ---------
@staff_member_required
def about_section(request):
    about = AboutSection.objects.first()
    return render(request, 'dashboard/about_section.html', {'about': about})

@staff_member_required
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

@staff_member_required
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
@staff_member_required
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

@staff_member_required
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

@staff_member_required
def delete_blog_category(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Blog category deleted successfully.')
        return redirect('blog_categories_list')
    return render(request, 'dashboard/blog_category_confirm_delete.html', {'category': category})

# -- -------- Blog Posts ---------
@staff_member_required
def blog_posts_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'dashboard/blog_posts_list.html', {'posts': posts})

@staff_member_required
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

@staff_member_required
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

@staff_member_required
def delete_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('blog_posts_list')
    return render(request, 'dashboard/blog_post_confirm_delete.html', {'post': post})

# -- -------- Testimonials ---------
@staff_member_required
def testimonials_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'dashboard/testimonials_list.html', {'testimonials': testimonials})

@staff_member_required
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

@staff_member_required
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

@staff_member_required
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

@staff_member_required
def instagram_sections_list(request):
    section = InstagramSection.objects.first()
    return render(request, 'dashboard/instagram_sections_list.html', {
        'section': section,
        'images': InstagramImage.objects.filter(section=section) if section else []
    })

@staff_member_required
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

@staff_member_required
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
@staff_member_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})


@staff_member_required
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


@staff_member_required
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


@staff_member_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')
    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})

# -- -------- Products ---------
@staff_member_required
def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'dashboard/product_list.html', {'products': products})


@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add Product'})


@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})


@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})

# -- -------- Coupons ---------
@staff_member_required
def coupons_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'dashboard/coupons_list.html', {'coupons': coupons})

@staff_member_required
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

@staff_member_required
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

@staff_member_required
def delete_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        messages.success(request, 'Coupon deleted successfully.')
        return redirect('coupons_list')
    return render(request, 'dashboard/coupon_confirm_delete.html', {'coupon': coupon})

# -- -------- Users ---------
@staff_member_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/users_list.html', {'users': users})

@staff_member_required
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

@staff_member_required
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

@staff_member_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('users_list')
    return render(request, 'dashboard/user_confirm_delete.html', {'user': user})

# -- -------- Wishlist Items ---------
@staff_member_required
def wishlist_items_list(request):
    items = WishlistItem.objects.select_related('user', 'product').all()
    return render(request, 'dashboard/wishlist_items_list.html', {'items': items})

@staff_member_required
def delete_wishlist_item(request, pk):
    item = get_object_or_404(WishlistItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Wishlist item deleted successfully.')
        return redirect('wishlist_items_list')
    return render(request, 'dashboard/wishlist_item_confirm_delete.html', {'item': item})

# -- -------- Orders ---------
@staff_member_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/order_list.html', {'orders': orders})

@staff_member_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'dashboard/order_detail.html', {'order': order})

@staff_member_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully.')
        return redirect('order_list')
    return render(request, 'dashboard/order_confirm_delete.html', {'order': order})

# -- -------- Team Members ---------
@staff_member_required
def team_members_list(request):
    members = TeamMember.objects.all()
    return render(request, 'dashboard/team_members_list.html', {'members': members})

@staff_member_required
def add_team_member(request):
    form = TeamMemberForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Team member added successfully.")
        return redirect('team_members_list')
    return render(request, 'dashboard/team_member_form.html', {'form': form, 'title': 'Add Team Member'})

@staff_member_required
def edit_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    form = TeamMemberForm(request.POST or None, request.FILES or None, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, "Team member updated successfully.")
        return redirect('team_members_list')
    return render(request, 'dashboard/team_member_form.html', {'form': form, 'title': 'Edit Team Member'})

@staff_member_required
def delete_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Team member deleted successfully.")
        return redirect('team_members_list')
    return render(request, 'dashboard/team_member_confirm_delete.html', {'member': member})

# -- -------- Map Location (Singleton) ---------
@staff_member_required
def maplocation_list(request):
    map_location = MapLocation.objects.first()
    return render(request, 'dashboard/maplocation_list.html', {'map_location': map_location, 'title': 'Map Location'})

@staff_member_required
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
@staff_member_required
def contactdetail_list(request):
    contact_detail = ContactDetail.objects.first()
    return render(request, 'dashboard/contactdetail_list.html', {'contact_detail': contact_detail, 'title': 'Contact Detail'})

@staff_member_required
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
@staff_member_required
def contact_messages_list(request):
    messages_list = ContactMessage.objects.order_by('-submitted_at')
    return render(request, 'dashboard/contact_messages_list.html', {
        'messages_list': messages_list,
        'title': 'Contact Messages'
    })

@staff_member_required
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
@staff_member_required
def newsletter_subscribers_list(request):
    subscribers = NewsletterSubscriber.objects.all()
    return render(request, 'dashboard/newsletter_subscribers_list.html', {'subscribers': subscribers})

def delete_newsletter_subscriber(request, pk):
    subscriber = get_object_or_404(NewsletterSubscriber, pk=pk)
    if request.method == 'POST':
        subscriber.delete()
        messages.success(request, '🗑️ Newsletter subscriber deleted successfully.')
        return redirect('newsletter_subscribers_list')
    return render(request, 'dashboard/newsletter_subscribers_confirm_delete.html', {
        'subscriber': subscriber
    })

@staff_member_required
def logout_view(request):
    logout(request)
    return redirect('home')

# -------- Special Offers ---------
@staff_member_required
def specialoffers_list(request):
    specialoffers = SpecialOffer.objects.all()
    return render(request, 'dashboard/specialoffers_list.html', {'specialoffers': specialoffers})

@staff_member_required
def add_specialoffer(request):
    if request.method == 'POST':
        form = SpecialOfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Special Offer added successfully!")
            return redirect('specialoffers_list')
    else:
        form = SpecialOfferForm()
    return render(request, 'dashboard/specialoffer_form.html', {'form': form, 'title': 'Add Special Offer'})

@staff_member_required
def edit_specialoffer(request, pk):
    specialoffer = get_object_or_404(SpecialOffer, pk=pk)
    if request.method == 'POST':
        form = SpecialOfferForm(request.POST, request.FILES, instance=specialoffer)
        if form.is_valid():
            form.save()
            messages.success(request, "Special Offer updated successfully!")
            return redirect('specialoffers_list')
    else:
        form = SpecialOfferForm(instance=specialoffer)
    return render(request, 'dashboard/specialoffer_form.html', {'form': form, 'title': 'Edit Special Offer'})

@staff_member_required
def delete_specialoffer(request, pk):
    specialoffer = get_object_or_404(SpecialOffer, pk=pk)
    if request.method == 'POST':
        specialoffer.delete()
        messages.success(request, "Special Offer deleted successfully!")
        return redirect('specialoffers_list')
    return render(request, 'dashboard/specialoffer_confirm_delete.html', {
        'specialoffer': specialoffer,
        'title': 'Delete Special Offer'
    })


# -------- Organization Details (Singleton) ---------
@staff_member_required
def organization_details(request):
    organization = OrganizationDetails.objects.first()
    return render(request, 'dashboard/organizationdetails_detail.html', {'organization': organization})

@staff_member_required
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

@staff_member_required
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