from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import (
    Product, Order, OrderItem, BlogPost, BlogComment,
    Coupon, NewsletterSubscriber, Category, ContactMessage, WishlistItem,
    ProductOption, ProductOptionPrice, UserProfile, FlashSale, FlashSaleItem
)
from decimal import Decimal
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    # User fields nested inside UserProfile
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserProfile
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'profile_picture', 'bio', 'facebook', 'instagram', 'twitter', 'linkedin'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update user fields
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

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

def apply_coupon(code, total):
    try:
        coupon = Coupon.objects.get(code=code)
        discount_percent = min(coupon.discount, Decimal('100.0'))
        discount_amount = (total * discount_percent) / Decimal('100.0')
        return discount_amount
    except Coupon.DoesNotExist:
        return Decimal('0.00')

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'product_id', 'quantity', 'size', 'eggless', 'sugarless', 'message']
        read_only_fields = ['product']
        
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, allow_null=True)
    order_items = OrderItemSerializer(many=True, source='items')

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'phone',
            'address', 'address_line2', 'city', 'province', 'postal_code',
            'notes', 'delivery_date', 'delivery_time', 'payment_method',
            'coupon_code', 'discount_amount', 'flash_discount', 'total_amount',
            'status', 'order_items'
        ]
        read_only_fields = ['id', 'user', 'status', 'discount_amount', 'flash_discount', 'total_amount']

    def create(self, validated_data):
        order_items_data = validated_data.pop('items', None)
        if order_items_data is None:
            raise serializers.ValidationError({'order_items': 'This field is required.'})
        
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        validated_data['user'] = user

        # Create the Order instance
        order = Order.objects.create(**validated_data)
        total = Decimal('0.00')

        # Create each OrderItem linked to the Order
        for item_data in order_items_data:
            product_id = item_data.pop('product_id')
            product = Product.objects.get(id=product_id)

            size = item_data.get('size')
            eggless = item_data.get('eggless', False)
            sugarless = item_data.get('sugarless', False)
            message = item_data.get('message', '')
            quantity = item_data['quantity']

            # Assuming you have a helper function to calculate item price
            price = calculate_item_price(product, size, eggless, sugarless)
            subtotal = price * quantity
            total += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                size=size,
                eggless=eggless,
                sugarless=sugarless,
                price=price,
                message=message
            )

        # Apply coupon and flash discount logic here (adjust as needed)
        coupon_code = validated_data.get('coupon_code')
        discount_amount = apply_coupon(coupon_code, total) if coupon_code else Decimal('0.00')
        flash_discount = Decimal(self.context['request'].session.get('flash_discount', '0.00'))

        final_total = total - discount_amount - flash_discount
        order.total_amount = max(final_total, Decimal('0.00'))
        order.discount_amount = discount_amount
        order.flash_discount = flash_discount
        order.save()

        # Remove flash discount from session if present
        if 'flash_discount' in self.context['request'].session:
            del self.context['request'].session['flash_discount']

        return order

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'content', 'author', 'image',
            'views', 'category', 'created_at'
        ]

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BlogComment
        fields = ['id', 'blog', 'user', 'comment', 'created_at']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'subscribed_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['id', 'user', 'product', 'added_at']
        read_only_fields = ['id', 'user', 'added_at']

class FlashSaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    original_price = serializers.DecimalField(source='product.price', max_digits=8, decimal_places=2, read_only=True)
    discount_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = FlashSaleItem
        fields = ['id', 'product', 'product_name', 'original_price', 'discounted_price', 'discount_percentage']

class FlashSaleSerializer(serializers.ModelSerializer):
    items = FlashSaleItemSerializer(many=True, read_only=True)

    class Meta:
        model = FlashSale
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'banner_image', 'items']