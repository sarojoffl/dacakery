from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Slider, Category, Product, AboutSection, TeamMember, Testimonial,
    InstagramSection, MapLocation, ContactDetail, WishlistItem, Order, OrderItem
)
from .forms import ContactForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

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

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html')

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

    return render(request, 'shoping_cart.html', {
        'cart_items': cart_items,
        'total': total,
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
        code = request.POST.get('coupon_code')
        # You can implement real coupon logic here
        messages.info(request, f'Coupon "{code}" applied!')
    return redirect('cart')

def checkout(request):
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        if not cart:
            messages.error(request, "Your cart is empty. Please add items before checking out.")
            return redirect('cart')  # or 'checkout'

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
            total_amount=total,
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

        # Clear cart
        request.session['cart'] = {}

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

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'success.html', {'order': order})