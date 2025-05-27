from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Slider, Category, Product, AboutSection, TeamMember, Testimonial,
    InstagramSection, MapLocation, ContactDetail, Coupon, WishlistItem, Order,
    OrderItem, BlogPost, BlogCategory, NewsletterSubscriber
)
from .forms import ContactForm, NewsletterForm
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from django.http import JsonResponse

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('login')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    
    return render(request, 'edit_profile.html', {'user': request.user})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_details.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

def home(request):
    sliders = Slider.objects.all()
    about = AboutSection.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all()[:8]
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    instagram_section = InstagramSection.objects.prefetch_related('images').first()
    map_location = MapLocation.objects.first()
    return render(request, 'home.html', {
        'sliders': sliders,
        'about': about,
        'categories': categories,
        'products': products,
        'team_members': team_members,
        'testimonials': testimonials,
        'instagram_section': instagram_section,
        'map_location': map_location,
    })

def about(request):
    about = AboutSection.objects.first()
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request, 'about.html', {
        'about': about,
        'team_members': team_members,
        'testimonials': testimonials,
    })

def contact(request):
    contact_detail = ContactDetail.objects.first()
    map_location = MapLocation.objects.first()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'map_location': map_location,
        'contact_detail': contact_detail,
        'form': form,
    })

def shop(request):
    products = Product.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort')

    if category_id:
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(Q(name__icontains=search_query))

    if sort_by == 'a_to_z':
        products = products.order_by('name')
    elif sort_by == 'price_low_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-price')

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': Category.objects.all(),
        'page_obj': page_obj,
        'total_results': products.count(),
    }
    return render(request, 'shop.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })

@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'{product.name} has been added to your wishlist.')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    try:
        wishlist_item = WishlistItem.objects.get(user=request.user, product=product)
        wishlist_item.delete()
        messages.success(request, f'{product.name} has been removed from your wishlist.')
    except WishlistItem.DoesNotExist:
        messages.error(request, f'{product.name} is not in your wishlist.')
    return redirect('wishlist')

def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    
    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    coupon_data = request.session.get('coupon')
    discount_percent = Decimal(str(coupon_data['discount'])) if coupon_data else Decimal('0.0')
    discount_percent = min(discount_percent, Decimal('100.0'))  # Cap at 100%

    discount = (total * discount_percent) / Decimal('100.0')
    discounted_total = total - discount

    return render(request, 'shoping_cart.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'discount_percent': discount_percent,
        'discounted_total': discounted_total,
        'coupon_code': coupon_data['code'] if coupon_data else '',
    })

def add_to_cart(request, slug):
    if request.method == "POST":
        product = get_object_or_404(Product, slug=slug)
        cart = request.session.get('cart', {})

        product_id = str(product.id)
        quantity = int(request.POST.get('quantity', 1))

        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        request.session['cart'] = cart
        messages.success(request, f"{product.name} added to cart!")
        return redirect('cart')
    else:
        return redirect('product_detail', slug=slug)

def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        # Loop through POST data and update quantities
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                try:
                    product_id = key.split('_')[1]
                    quantity = int(value)
                    if quantity < 1:
                        continue
                    if product_id in cart:
                        cart[product_id] = quantity
                except (ValueError, IndexError):
                    continue

        request.session['cart'] = cart
        messages.success(request, 'Cart updated successfully.')

    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')

def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip()
        cart = request.session.get('cart', {})

        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')

        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            request.session['coupon'] = {
                'code': coupon.code,
                'discount': float(coupon.discount),  # store discount as a float
            }
            messages.success(request, f"Coupon '{coupon.code}' applied successfully!")
        except Coupon.DoesNotExist:
            request.session.pop('coupon', None)
            messages.error(request, "Invalid or expired coupon code.")

    return redirect('cart')

def checkout(request):
    cart = request.session.get('cart', {})

    coupon_data = request.session.get('coupon', None)
    discount_percent = Decimal(str(coupon_data['discount'])) if coupon_data else Decimal('0.0')
    discount_percent = min(discount_percent, Decimal('100.0'))
    coupon_code = coupon_data['code'] if coupon_data else ''

    if request.method == 'POST':
        if not cart:
            messages.error(request, "Your cart is empty. Please add items before checking out.")
            return redirect('cart')

        user = request.user if request.user.is_authenticated else None

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        notes = request.POST.get('notes', '')
        payment_method = request.POST.get('payment_method', 'cod')

        # Handle account creation
        create_account = request.POST.get('create_account')
        account_password = request.POST.get('account_password')

        if create_account and not user:
            if User.objects.filter(username=email).exists():
                messages.error(request, "User with this email already exists. Please log in.")
                return redirect('checkout')
            if not account_password:
                messages.error(request, "Please enter a password to create an account.")
                return redirect('checkout')

            user = User.objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(account_password)
            )

        # Calculate total
        total = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total += product.price * quantity

        discount_amount = (total * discount_percent) / Decimal('100.0')
        final_total = total - discount_amount

        # Create Order
        order = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            country=country,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            zip=zip_code,
            phone=phone,
            email=email,
            notes=notes,
            payment_method=payment_method,
            total_amount=final_total,
            coupon_code=coupon_code,
            discount_amount=discount_amount,
        )

        # Create Order Items
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

        # Clear cart and discount session
        request.session['cart'] = {}
        request.session.pop('coupon', None)  # fixed from 'discount' to 'coupon'

        return redirect('order_success', order_id=order.id)

    # GET request: prepare cart data
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    discount_amount = (total * discount_percent) / Decimal('100.0')
    final_total = total - discount_amount

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'final_total': final_total,
        'discount_amount': discount_amount,
        'discount_percent': discount_percent,
        'coupon_code': coupon_code,
    })

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'success.html', {'order': order})

def blog_list(request):
    blogs = BlogPost.objects.select_related('category').order_by('-created_at')

    # Annotate categories with blog post counts
    categories = BlogCategory.objects.annotate(count=Count('blog_posts'))

    recent_blogs = blogs[:5]  # For sidebar

    context = {
        'blogs': blogs,
        'recent_blogs': recent_blogs,
        'categories': categories,
    }
    return render(request, 'blog.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

def newsletter_signup_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                return JsonResponse({'status': 'success', 'message': 'Thanks for subscribing!'})
            else:
                return JsonResponse({'status': 'info', 'message': 'You are already subscribed.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid email.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})