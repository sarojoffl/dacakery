from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Slider, Category, Product, AboutSection, TeamMember, Testimonial,
    InstagramSection, MapLocation, ContactDetail, Coupon, WishlistItem, Order,
    OrderItem, BlogPost, BlogCategory, NewsletterSubscriber, SpecialOffer
)
from .forms import ContactForm, BlogCommentForm
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
from django.utils.timezone import now
from datetime import date
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('dashboard_home')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')

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

    return render(request, 'core/register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def edit_profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        # Update User fields
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        # Update UserProfile fields
        profile.bio = request.POST.get('bio')
        profile.facebook = request.POST.get('facebook')
        profile.instagram = request.POST.get('instagram')
        profile.twitter = request.POST.get('twitter')

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'core/edit_profile.html', {'user': user})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/order_details.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})

def home(request):
    sliders = Slider.objects.all()
    about = AboutSection.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all()[:8]
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    instagram_section = InstagramSection.objects.prefetch_related('images').first()
    map_location = MapLocation.objects.first()
    special_offers = SpecialOffer.objects.filter(
        valid_until__gte=now().date()
    ) | SpecialOffer.objects.filter(valid_until__isnull=True)  # include offers without an expiry
    
    return render(request, 'core/home.html', {
        'sliders': sliders,
        'about': about,
        'categories': categories,
        'products': products,
        'team_members': team_members,
        'testimonials': testimonials,
        'instagram_section': instagram_section,
        'map_location': map_location,
        'special_offers': special_offers,
    })

def about(request):
    about = AboutSection.objects.first()
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request, 'core/about.html', {
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

    return render(request, 'core/contact.html', {
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
    return render(request, 'core/shop.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]
    return render(request, 'core/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'core/wishlist.html', {'wishlist_items': wishlist_items})

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

EXTRA_PRICES = {
    'eggless': Decimal('150.0'),
    'sugarless': Decimal('100.0'),
    'size': {
        '0.5': Decimal('0.5'),
        '1': Decimal('1.0'),
        '2': Decimal('2.0')
    }
}

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0')

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue

        # Fix here: check if item is dict, else assume quantity as int
        if isinstance(item, dict):
            quantity = item.get('quantity', 1)
            size = item.get('size', '1')
            eggless = item.get('eggless', False)
            sugarless = item.get('sugarless', False)
            message = item.get('message')
        else:
            # Item is just quantity (int)
            quantity = item
            size = '1'  # default size
            eggless = False
            sugarless = False
            message = ''

        # Base price adjustments
        base_price = product.price * EXTRA_PRICES['size'].get(size, Decimal('1.0'))

        if eggless:
            base_price += EXTRA_PRICES['eggless']
        if sugarless:
            base_price += EXTRA_PRICES['sugarless']

        subtotal = base_price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'eggless': eggless,
            'sugarless': sugarless,
            'size': size,
            'message': message,
            'subtotal': subtotal
        })

    coupon_data = request.session.get('coupon')
    discount_percent = Decimal(str(coupon_data['discount'])) if coupon_data else Decimal('0.0')
    discount_percent = min(discount_percent, Decimal('100.0'))
    discount = (total * discount_percent) / Decimal('100.0')
    discounted_total = total - discount

    return render(request, 'core/shoping_cart.html', {
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
        eggless = request.POST.get('eggless') == 'on'
        sugarless = request.POST.get('sugarless') == 'on'
        size = request.POST.get('size')
        message = request.POST.get('message')

        item = {
            'quantity': quantity,
            'eggless': eggless,
            'sugarless': sugarless,
            'size': size,
            'message': message
        }

        cart[product_id] = item
        request.session['cart'] = cart
        messages.success(request, f"{product.name} added to cart!")
        return redirect('cart')
    else:
        return redirect('product_detail', slug=slug)


def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                try:
                    product_id = key.split('_')[1]
                    quantity = int(value)
                    if quantity < 1:
                        # Remove item if quantity less than 1
                        if product_id in cart:
                            del cart[product_id]
                    else:
                        if product_id in cart:
                            # Update quantity inside the cart item dict
                            cart[product_id]['quantity'] = quantity
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

def calculate_item_price(product, size='1', eggless=False, sugarless=False):
    price = product.price * EXTRA_PRICES['size'].get(size, Decimal('1.0'))
    if eggless:
        price += EXTRA_PRICES['eggless']
    if sugarless:
        price += EXTRA_PRICES['sugarless']
    return price

def checkout(request):
    cart = request.session.get('cart', {})
    coupon_data = request.session.get('coupon')
    discount_percent = Decimal(str(coupon_data['discount'])) if coupon_data else Decimal('0.0')
    discount_percent = min(discount_percent, Decimal('100.0'))
    coupon_code = coupon_data['code'] if coupon_data else ''

    if request.method == 'POST':
        if not cart:
            messages.error(request, "Your cart is empty. Please add items before checking out.")
            return redirect('cart')

        user = request.user if request.user.is_authenticated else None

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        country = request.POST.get('country', '').strip()
        address_line1 = request.POST.get('address_line1', '').strip()
        address_line2 = request.POST.get('address_line2', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        zip_code = request.POST.get('zip', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        notes = request.POST.get('notes', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')
        delivery_date = request.POST.get('delivery_date')
        delivery_time = request.POST.get('delivery_time')

        if delivery_date and date.fromisoformat(delivery_date) < date.today():
            messages.error(request, "Delivery date cannot be in the past.")
            return redirect('checkout')

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

        total = Decimal('0')
        order_items = []

        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            if isinstance(item, dict):
                quantity = int(item.get('quantity', 1))
                size = item.get('size', '1')
                eggless = item.get('eggless', False)
                sugarless = item.get('sugarless', False)
                message = item.get('message', '')
            else:
                quantity = int(item)
                size = '1'
                eggless = False
                sugarless = False
                message = ''

            price = calculate_item_price(product, size, eggless, sugarless)
            subtotal = price * quantity
            total += subtotal

            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'size': size,
                'eggless': eggless,
                'sugarless': sugarless,
                'delivery_date': delivery_date,
                'delivery_time': delivery_time,
                'message': message
            })

        discount_amount = (total * discount_percent) / Decimal('100.0')
        final_total = total - discount_amount

        # Create order and order items
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
            delivery_date=delivery_date,
            delivery_time=delivery_time,
        )

        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
                eggless=item['eggless'],
                sugarless=item['sugarless'],
                size=item['size'],
                message=item['message'],
            )

        # Clear cart
        request.session['cart'] = {}
        request.session.pop('coupon', None)

        # 🔁 Handle Khalti Payment
        if payment_method == 'khalti':
            headers = {
                'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
                'Content-Type': 'application/json',
            }
            payload = {
                'return_url': settings.KHALTI_RETURN_URL,
                'website_url': 'http://127.0.0.1:8000/',
                'amount': int(final_total * 100),  # in paisa
                'purchase_order_id': str(order.id),
                'purchase_order_name': f'Order {order.id}',
                'customer_info': {
                    'name': f'{first_name} {last_name}',
                    'email': email,
                    'phone': phone,
                },
            }

            response = requests.post(settings.KHALTI_INITIATE_URL, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                payment_url = data.get('payment_url')
                order.payment_id = data.get('pidx')
                order.save()
                return redirect(payment_url)
            else:
                print("Khalti Error Response:", response.status_code, response.text)
                messages.error(request, 'Error initiating payment with Khalti.')
                return redirect('checkout')

        # ✅ COD or other method
        return redirect('order_success', order_id=order.id)

    # For GET request: show cart summary
    cart_items = []
    total = Decimal('0')
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)

        if isinstance(item, dict):
            quantity = int(item.get('quantity', 1))
            size = item.get('size', '1')
            eggless = item.get('eggless', False)
            sugarless = item.get('sugarless', False)
        else:
            quantity = int(item)
            size = '1'
            eggless = False
            sugarless = False

        price = calculate_item_price(product, size, eggless, sugarless)
        subtotal = price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'size': size,
            'eggless': eggless,
            'sugarless': sugarless,
            'subtotal': subtotal,
        })

    discount_amount = (total * discount_percent) / Decimal('100.0')
    final_total = total - discount_amount

    return render(request, 'core/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'final_total': final_total,
        'discount_amount': discount_amount,
        'discount_percent': discount_percent,
        'coupon_code': coupon_code,
    })

@csrf_exempt
def verify_payment(request):
    pidx = request.GET.get('pidx')
    if not pidx:
        return HttpResponse('Missing pidx', status=400)

    headers = {
        'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {'pidx': pidx}

    response = requests.post(settings.KHALTI_LOOKUP_URL, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("Khalti verify response data:", data)  # debug print

        status = data.get('status')

        # Find order by payment_id (pidx)
        try:
            order = Order.objects.get(payment_id=pidx)
        except Order.DoesNotExist:
            return HttpResponse(f'Order with payment ID {pidx} not found', status=400)

        if status == 'Completed':
            order.status = 'paid'
            order.save()
            return redirect('order_success', order_id=order.id)
        else:
            order.status = 'failed'
            order.save()
            return redirect('order_failed', order_id=order.id)
    else:
        return HttpResponse('Error verifying payment', status=500)

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'core/success.html', {'order': order})

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
    return render(request, 'core/blog.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    blog.views += 1
    blog.save(update_fields=['views'])

    author_profile = getattr(blog.author, 'userprofile', None) if blog.author else None

    prev_blog = BlogPost.objects.filter(pk__lt=pk).order_by('-pk').first()
    next_blog = BlogPost.objects.filter(pk__gt=pk).order_by('pk').first()

    comments = blog.comments.all().order_by('-created_at')
    comment_form = BlogCommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = BlogCommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.blog = blog
                new_comment.user = request.user
                new_comment.save()
                return redirect('blog_detail', pk=pk)
        else:
            return redirect('login')

    context = {
        'blog': blog,
        'author_profile': author_profile,
        'prev_blog': prev_blog,
        'next_blog': next_blog,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'core/blog_detail.html', context)

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

def search_results(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        # Example: search Products by name or description containing the query (case insensitive)
        results = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'core/search_results.html', context)