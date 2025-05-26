from .models import Product

def cart_summary(request):
    cart = request.session.get('cart', {})
    total = 0
    item_count = 0

    try:
        products = Product.objects.filter(id__in=cart.keys())

        for product in products:
            quantity = cart.get(str(product.id), 0)
            subtotal = product.price * quantity
            total += subtotal
            item_count += quantity
    except:
        pass  # Fails silently if Product table doesn't exist (e.g., during migrations)

    return {
        'cart_total': total,
        'cart_item_count': item_count
    }
