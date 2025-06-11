from datetime import date
import json
import hmac
import hashlib
import base64
import uuid
import requests

from decimal import Decimal

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from .models import (
    Slider, Category, Product, AboutSection, TeamMember, Testimonial,
    InstagramSection, MapLocation, ContactDetail, Coupon, WishlistItem, Order,
    OrderItem, BlogPost, BlogCategory, NewsletterSubscriber, FlashSale,
    ProductOption, ProductOptionPrice, CouponUsage
)
from .forms import ContactForm, BlogCommentForm


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect admins to dashboard, others to home
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

        # Password match validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Unique username and email validation
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        # Create and save new user
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

        # Update profile picture if uploaded
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'core/edit_profile.html', {'user': user})


@login_required
def order_list(request):
    # Fetch orders of logged-in user, latest first
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/order_details.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    # Get specific order belonging to user or 404
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})


def home(request):
    # Load homepage sections from DB
    sliders = Slider.objects.all()
    about = AboutSection.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all()[:8]  # Top 8 products
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    instagram_section = InstagramSection.objects.prefetch_related('images').first()
    map_location = MapLocation.objects.first()

    # Get only active flash sales
    current_time = now()
    flashsales = FlashSale.objects.filter(start_time__lte=current_time, end_time__gte=current_time).prefetch_related('items__product')

    return render(request, 'core/home.html', {
        'sliders': sliders,
        'about': about,
        'categories': categories,
        'products': products,
        'team_members': team_members,
        'testimonials': testimonials,
        'instagram_section': instagram_section,
        'map_location': map_location,
        'flashsales': flashsales,
    })


def about(request):
    # About page content
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

    # Filter by category
    if category_id:
        products = products.filter(category_id=category_id)

    # Filter by search query
    if search_query:
        products = products.filter(Q(name__icontains=search_query))

    # Sort products
    if sort_by == 'a_to_z':
        products = products.order_by('name')
    elif sort_by == 'price_low_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-price')

    # Pagination: 8 items per page
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

    # Get all ProductOptionPrice entries for this product
    option_prices = ProductOptionPrice.objects.filter(product=product).select_related('option')
    option_price_dict = {op.option.id: op.price for op in option_prices}

    size_options = []
    extra_options = []

    for option in ProductOption.objects.all():
        price = option_price_dict.get(option.id, option.default_price)
        option_data = {'option': option, 'price': price}

        if option.type == 'size':
            size_options.append(option_data)
        elif option.type == 'extra':
            extra_options.append(option_data)

    current_price = product.get_current_price()

    return render(request, 'core/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'size_options': size_options,
        'extra_options': extra_options,
        'current_price': current_price,
    })


@login_required
def wishlist(request):
    # Show user's wishlist items
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'core/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    # Notify if added or already exists
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
    cart_items = []
    total = Decimal('0')
    flash_discount = Decimal('0')

    # Iterate over item_key and item_details to process cart contents
    for item_key, item_details in list(cart.items()): 
        product_id = item_details.get('product_id')

        if not product_id:
            messages.error(request, f"Invalid item in cart. Removing: {item_key}")
            del request.session['cart'][item_key]
            request.session.modified = True 
            continue 

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.warning(request, f"A product in your cart (ID: {product_id}) no longer exists and has been removed.")
            del request.session['cart'][item_key]
            request.session.modified = True
            continue 

        quantity = item_details.get('quantity', 1)
        size = item_details.get('size', '1')
        eggless = item_details.get('eggless', False)
        sugarless = item_details.get('sugarless', False)
        message = item_details.get('message')

        price = calculate_item_price(product, size=size, eggless=eggless, sugarless=sugarless)
        subtotal = price * quantity
        total += subtotal

        original_price = product.price or Decimal('0')
        current_price = product.get_current_price() or Decimal('0')
        item_flash_discount = max(original_price - current_price, Decimal('0')) * quantity
        flash_discount += item_flash_discount

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'eggless': eggless,
            'sugarless': sugarless,
            'size': size,
            'message': message,
            'subtotal': subtotal,
            'item_key': item_key 
        })

    request.session['cart_total'] = str(total)

    coupon_data = request.session.get('coupon')
    applied_discount = Decimal('0.0')
    coupon_code_display = ''

    if coupon_data:
        try:
            coupon = Coupon.objects.get(code__iexact=coupon_data['code'])

            if not coupon.active:
                messages.warning(request, f"Coupon '{coupon.code}' is no longer active and has been removed.")
                request.session.pop('coupon', None)
                coupon_data = None 
            elif coupon.valid_until and coupon.valid_until < timezone.now().date():
                messages.warning(request, f"Coupon '{coupon.code}' has expired and has been removed.")
                request.session.pop('coupon', None)
                coupon_data = None
            elif coupon.usage_limit is not None and coupon.times_used >= coupon.usage_limit:
                messages.warning(request, f"Coupon '{coupon.code}' has reached its usage limit and has been removed.")
                request.session.pop('coupon', None)
                coupon_data = None
            elif coupon.min_cart_value is not None and total < coupon.min_cart_value:
                messages.warning(request, f"Coupon '{coupon.code}' requires a minimum cart value of रु {coupon.min_cart_value}. It has been removed.")
                request.session.pop('coupon', None)
                coupon_data = None
            else:
                coupon_code_display = coupon.code
                discount_percent = Decimal(str(coupon.discount))
                applied_discount = (total * discount_percent) / Decimal('100.0')

                if coupon.max_discount_amount is not None:
                    max_discount_amount = Decimal(str(coupon.max_discount_amount))
                    applied_discount = min(applied_discount, max_discount_amount)

        except Coupon.DoesNotExist:
            messages.warning(request, "Applied coupon code is invalid or no longer exists. It has been removed.")
            request.session.pop('coupon', None)
            coupon_data = None

    discounted_total = total - applied_discount

    request.session['flash_discount'] = str(flash_discount)

    coupons = Coupon.objects.filter(active=True)
    show_coupon_section = False
    for coupon in coupons:
        if coupon.min_cart_value is None or total >= coupon.min_cart_value:
            show_coupon_section = True
            break

    # Fetch all active coupons and filter by min_cart_value
    available_coupons = Coupon.objects.filter(active=True).filter(
        Q(min_cart_value__isnull=True) | Q(min_cart_value__lte=total)
    )
    
    return render(request, 'core/shoping_cart.html', {
        'cart_items': cart_items,
        'total': total,
        'show_coupon_section': show_coupon_section,
        'available_coupons': available_coupons,
        'flash_discount': flash_discount,
        'discount': applied_discount,
        'discount_percent': Decimal(str(coupon_data['discount'])) if coupon_data else Decimal('0.0'),
        'discounted_total': discounted_total,
        'coupon_code': coupon_code_display,
    })


def add_to_cart(request, slug):
    if request.method == "POST":
        product = get_object_or_404(Product, slug=slug)
        cart = request.session.get('cart', {})

        quantity = int(request.POST.get('quantity', 1))
        eggless = request.POST.get('eggless') == 'on'
        sugarless = request.POST.get('sugarless') == 'on'
        size = request.POST.get('size')
        message = request.POST.get('message', '').strip()

        if not size:
            size = 'Medium'

        # Create a unique key to differentiate product configurations
        item_key = f"{product.id}-{size}-{eggless}-{sugarless}"

        new_item_details = {
            'quantity': quantity,
            'eggless': eggless,
            'sugarless': sugarless,
            'size': size,
            'message': message,
            'product_id': str(product.id)
        }

        if item_key in cart:
            cart[item_key]['quantity'] += quantity
            if message:
                 cart[item_key]['message'] = message
            messages.info(request, f"Quantity for '{product.name}' ({size}) updated in cart!")
        else:
            cart[item_key] = new_item_details
            messages.success(request, f"'{product.name}' ({size}) added to cart!")

        request.session['cart'] = cart
        if 'coupon' in request.session:
            messages.info(request, "Cart contents changed. Coupon may need re-evaluation.")
            request.session.pop('coupon', None)

        return redirect('cart')
    else:
        return redirect('product_detail', slug=slug)


def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        cart_changed_significantly = False 

        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                try:
                    qty = int(value)
                    if product_id in cart:
                        current_qty = cart[product_id].get('quantity', 1)
                        if qty < 1:
                            cart.pop(product_id, None)
                            if current_qty > 0:
                                cart_changed_significantly = True
                        elif qty != current_qty:
                            cart[product_id]['quantity'] = qty
                            cart_changed_significantly = True
                except ValueError:
                    continue

        request.session['cart'] = cart

        if cart_changed_significantly:
            if 'coupon' in request.session:
                # Use messages.info to let the user know the coupon might be re-evaluated
                messages.info(request, "Cart updated. Coupon re-evaluation needed.") 
            request.session.pop('coupon', None)

        messages.success(request, 'Cart updated successfully.')
    return redirect('cart')


def remove_from_cart(request, item_key):
    cart = request.session.get('cart', {})

    if item_key in cart:
        cart.pop(item_key)
        request.session['cart'] = cart
        # Invalidate coupon as cart contents have changed
        if 'coupon' in request.session:
            messages.info(request, "Cart contents changed. Coupon may need re-evaluation.")
            request.session.pop('coupon', None)
        request.session.modified = True
        messages.success(request, 'Item removed from cart.')
    else:
        messages.error(request, 'Item not found in cart.')

    return redirect('cart')

def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip()
        cart = request.session.get('cart', {})
        cart_total = Decimal(request.session.get('cart_total', '0.00'))

        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')

        if not request.user.is_authenticated:
            messages.error(request, "Please log in to use a coupon.")
            return redirect('login')  # Or wherever your login page is

        try:
            coupon = Coupon.objects.get(code__iexact=code)

            # Check if coupon is active and valid date
            if not coupon.active:
                messages.error(request, "This coupon is no longer active.")
                request.session.pop('coupon', None)
                return redirect('cart')

            if coupon.valid_until and coupon.valid_until < timezone.now().date():
                messages.error(request, "This coupon has expired.")
                request.session.pop('coupon', None)
                return redirect('cart')

            # Check overall usage limit
            if coupon.usage_limit is not None and coupon.times_used >= coupon.usage_limit:
                messages.error(request, "This coupon has reached its usage limit.")
                request.session.pop('coupon', None)
                return redirect('cart')

            # Check minimum cart value
            if coupon.min_cart_value is not None and cart_total < coupon.min_cart_value:
                messages.error(request, f"Minimum cart value for this coupon is रु {coupon.min_cart_value}.")
                request.session.pop('coupon', None)
                return redirect('cart')

            # Check if user has already used this coupon
            if CouponUsage.objects.filter(user=request.user, coupon=coupon).exists():
                messages.error(request, "You have already used this coupon.")
                request.session.pop('coupon', None)
                return redirect('cart')

            # Passed all checks — apply coupon in session
            request.session['coupon'] = {
                'code': coupon.code,
                'discount': float(coupon.discount),
                'max_discount_amount': float(coupon.max_discount_amount) if coupon.max_discount_amount else None,
            }
            messages.success(request, f"Coupon '{coupon.code}' applied successfully!")

        except Coupon.DoesNotExist:
            request.session.pop('coupon', None)
            messages.error(request, "Invalid coupon code.")

    return redirect('cart')


def get_option_price(product, option_name, option_type):
    try:
        option = ProductOption.objects.get(name__iexact=option_name, type=option_type)
    except ProductOption.DoesNotExist:
        return Decimal('1.00') if option_type == 'size' else Decimal('0.00')

    try:
        option_price = ProductOptionPrice.objects.get(product=product, option=option)
        return option_price.price
    except ProductOptionPrice.DoesNotExist:
        return option.default_price or (Decimal('1.00') if option_type == 'size' else Decimal('0.00'))


def calculate_item_price(product, size=None, eggless=False, sugarless=False):
    price = product.get_current_price() or Decimal('0.00')

    if size:
        price *= get_option_price(product, size, 'size')

    if eggless:
        price += get_option_price(product, 'Eggless', 'extra')

    if sugarless:
        price += get_option_price(product, 'Sugarless', 'extra')

    return price


def generate_esewa_signature(secret_key, data_dict, signed_fields):
    # Create HMAC SHA256 signature and encode it in base64 for eSewa payment verification
    message = ",".join(f"{field}={data_dict[field]}" for field in signed_fields)
    secret_key_bytes = secret_key.encode('utf-8')
    message_bytes = message.encode('utf-8')

    signature = hmac.new(secret_key_bytes, message_bytes, hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')

    return signature_b64


def checkout(request):
    cart = request.session.get('cart', {})
    coupon_data = request.session.get('coupon')
    discount_percent = Decimal(str(coupon_data['discount'])) if coupon_data else Decimal('0.0')
    discount_percent = min(discount_percent, Decimal('100.0'))  # Cap discount at 100%
    coupon_code = coupon_data['code'] if coupon_data else ''

    if request.method == 'POST':
        if not cart:
            messages.error(request, "Your cart is empty. Please add items before checking out.")
            return redirect('cart')

        user = request.user if request.user.is_authenticated else None

        # Get customer and order details from POST data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        address = request.POST.get('address', '').strip()
        address_line2 = request.POST.get('address_line2', '').strip()
        city = request.POST.get('city', '').strip()
        province = request.POST.get('state', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        notes = request.POST.get('notes', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')
        delivery_date = request.POST.get('delivery_date')
        delivery_time = request.POST.get('delivery_time')

        # Validate delivery date (cannot be in the past)
        if delivery_date and date.fromisoformat(delivery_date) < date.today():
            messages.error(request, "Delivery date cannot be in the past.")
            return redirect('checkout')

        # Account creation logic if user opts in
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

        for item_key, item_details in cart.items(): # Iterate over item_key and its details
            product_id = item_details.get('product_id') # Extract product_id from the details
            if not product_id:
                # Handle cases where product_id might be missing (shouldn't happen with current add_to_cart)
                messages.error(request, f"Corrupted cart item detected. Removing: {item_key}")
                del request.session['cart'][item_key]
                request.session.modified = True
                continue
            
            product = get_object_or_404(Product, id=product_id) # Use the extracted product_id
            quantity = int(item_details.get('quantity', 1))
            size = item_details.get('size')
            eggless = item_details.get('eggless', False)
            sugarless = item_details.get('sugarless', False)
            message = item_details.get('message', '')

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

        flash_discount = Decimal(request.session.get('flash_discount', '0'))

        # Create order in DB
        order = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            address_line2=address_line2,
            city=city,
            province=province,
            postal_code=postal_code,
            notes=notes,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            payment_method=payment_method,
            coupon_code=coupon_code,
            discount_amount=discount_amount,
            flash_discount=flash_discount,
            total_amount=final_total,
        )

        if 'flash_discount' in request.session:
            del request.session['flash_discount']

        # Create individual order items in DB
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
                size=item['size'],
                eggless=item['eggless'],
                sugarless=item['sugarless'],
                message=item['message'],
            )

        # Payment method: Khalti
        if payment_method == 'khalti':
            headers = {
                'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
                'Content-Type': 'application/json',
            }
            payload = {
                'return_url': settings.KHALTI_RETURN_URL,
                'website_url': settings.SITE_URL,
                'amount': int(final_total * 100),  # amount in paisa
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
                messages.error(request, 'Error initiating payment with Khalti.')
                return redirect('checkout')

        # Payment method: eSewa
        elif payment_method == 'esewa':
            transaction_uuid = str(uuid.uuid4())
            base_url = settings.ESEWA_RETURN_URL.rstrip('/')
            esewa_data = {
                'amount': str(order.total_amount),
                'tax_amount': '0',
                'total_amount': str(order.total_amount),
                'transaction_uuid': transaction_uuid,
                'product_code': settings.ESEWA_PRODUCT_CODE,
                'product_service_charge': '0',
                'product_delivery_charge': '0',
                'success_url': f"{base_url}/{order.id}/q/su/",
                'failure_url': f"{base_url}/{order.id}/q/fu/",
                'signed_field_names': 'total_amount,transaction_uuid,product_code',
            }

            # Generate signature for eSewa payment data
            signed_fields = esewa_data['signed_field_names'].split(',')
            signature = generate_esewa_signature(settings.ESEWA_SECRET_KEY, esewa_data, signed_fields)
            esewa_data['signature'] = signature

            return render(request, 'payment/esewa_redirect_v2.html', {'esewa_data': esewa_data})

        # Clear cart and coupon after successful order placement (for COD)
        request.session['cart'] = {}
        request.session.pop('coupon', None)

        # After order creation for COD:
        if payment_method == 'cod' and coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                coupon.increment_usage()
                CouponUsage.objects.create(
                    user=user,
                    coupon=coupon,
                    order=order
                )
            except Coupon.DoesNotExist:
                pass  # handle logging or ignore

        return redirect('order_success', order_id=order.id)

    # Render checkout page with cart summary if GET request
    cart_items = []
    total = Decimal('0')

    for item_key, item_details in cart.items(): # Iterate over item_key and its details
        product_id = item_details.get('product_id') # Extract product_id from the details
        if not product_id:
            messages.error(request, f"Invalid item '{item_key}' found in your cart. Please clear your cart or re-add items.")
            continue # Skip this invalid item for display
        
        product = get_object_or_404(Product, id=product_id) # Use the extracted product_id
        quantity = int(item_details.get('quantity', 1))
        size = item_details.get('size')
        eggless = item_details.get('eggless', False)
        sugarless = item_details.get('sugarless', False)

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
        'ESEWA_PAYMENT_URL': settings.ESEWA_PAYMENT_URL,
    })


@csrf_exempt
def esewa_verify(request, oid, status):
    order = get_object_or_404(Order, id=oid)
    refId = request.GET.get('refId')

    # Handle base64 encoded data from eSewa callback
    if not refId and 'data' in request.GET:
        try:
            decoded_data = base64.b64decode(request.GET['data']).decode('utf-8')
            data_json = json.loads(decoded_data)
            refId = data_json.get('transaction_uuid')
            status = 'su' if data_json.get('status') == 'COMPLETE' else 'failed'
        except Exception:
            order.status = 'failed'
            order.save()
            return redirect('order_failed', order_id=order.id)

    # Mark order as paid if successful
    if status == 'su' and refId:
        order.status = 'paid'
        order.payment_id = refId
        order.save()

        request.session['cart'] = {}
        request.session.pop('coupon', None)
        
        if status == 'su' and order.status == 'paid':
            if order.coupon_code:
                try:
                    coupon = Coupon.objects.get(code=order.coupon_code)
                    coupon.increment_usage()
                    CouponUsage.objects.create(
                        user=order.user,
                        coupon=coupon,
                        order=order
                    )
                except Coupon.DoesNotExist:
                    pass

        return redirect('order_success', order_id=order.id)

    # Mark order as failed otherwise
    order.status = 'failed'
    order.save()
    return redirect('order_failed', order_id=order.id)


@csrf_exempt
def khalti_verify(request):
    pidx = request.GET.get('pidx')
    if not pidx:
        return HttpResponse('Missing pidx', status=400)

    try:
        order = Order.objects.get(payment_id=pidx)
    except Order.DoesNotExist:
        return HttpResponse(f'Order with payment ID {pidx} not found', status=400)

    headers = {
        'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {'pidx': pidx}

    response = requests.post(settings.KHALTI_LOOKUP_URL, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        status = data.get('status')

        if status == 'Completed':
            order.status = 'paid'
            order.save()

            # Clear cart and coupon after successful payment
            request.session['cart'] = {}
            request.session.pop('coupon', None)

            if status == 'Completed':
                if order.coupon_code:
                    try:
                        coupon = Coupon.objects.get(code=order.coupon_code)
                        coupon.increment_usage()
                        CouponUsage.objects.create(
                            user=order.user,
                            coupon=coupon,
                            order=order
                        )
                    except Coupon.DoesNotExist:
                        pass

            return redirect('order_success', order_id=order.id)
        else:
            order.status = 'failed'
            order.save()
            return redirect('order_failed', order_id=order.id)
    else:
        order.status = 'failed'
        order.save()
        return redirect('order_failed', order_id=order.id)

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payment/success.html', {'order': order})

def order_failed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payment/failure.html', {'order': order})

def blog_list(request):
    category_id = request.GET.get('category')
    
    blogs = BlogPost.objects.select_related('category').order_by('-created_at')
    
    if category_id:
        blogs = blogs.filter(category_id=category_id)

    categories = BlogCategory.objects.annotate(count=Count('blog_posts'))
    popular_blogs = BlogPost.objects.order_by('-views')[:5]

    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'blogs': page_obj,
        'popular_blogs': popular_blogs,
        'categories': categories,
        'page_obj': page_obj,
    }
    return render(request, 'core/blog.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    # Increment the blog's view count
    blog.views += 1
    blog.save(update_fields=['views'])

    author_profile = getattr(blog.author, 'userprofile', None) if blog.author else None

    # Get previous and next blog posts for navigation
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
        # Search products by name or description (case-insensitive)
        results = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'core/search_results.html', context)