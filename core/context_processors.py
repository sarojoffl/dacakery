from .models import Product
from .models import OrganizationDetails

def cart_summary(request):
    cart = request.session.get('cart', {})
    total = 0
    item_count = 0

    try:
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            item = cart.get(str(product.id), {})
            # item is a dict, get quantity safely
            quantity = item.get('quantity', 0) if isinstance(item, dict) else 0

            total += product.price * quantity
            item_count += quantity
    except Exception:
        pass  # Fail silently, e.g. migrations

    return {
        'cart_total': total,
        'cart_item_count': item_count,
    }


def organization_details(request):
    # Assuming there is only one OrganizationDetails instance
    organization = OrganizationDetails.objects.first()
    return {
        'organization': organization
    }