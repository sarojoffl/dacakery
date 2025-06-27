# Imports
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

import requests
import uuid
import hmac
import hashlib
import base64
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status as drf_status
from django.utils.timezone import now

# Models
from core.models import (
    Product, Order, BlogPost, BlogComment, Coupon, CouponUsage, NewsletterSubscriber,
    Category, ContactMessage, WishlistItem, FlashSale
)

# Serializers
from .serializers import (
    ProductSerializer, OrderSerializer, BlogPostSerializer, CommentSerializer,
    CouponSerializer, NewsletterSubscriberSerializer, UserProfileSerializer,
    CategorySerializer, ContactMessageSerializer, WishlistItemSerializer,
    RegisterSerializer, FlashSaleSerializer
)


# Utility function
def generate_esewa_signature(secret_key, data_dict, signed_fields):
    """
    Create HMAC SHA256 signature and encode it in base64 for eSewa payment verification
    """
    message = ",".join(f"{field}={data_dict[field]}" for field in signed_fields)
    secret_key_bytes = secret_key.encode('utf-8')
    message_bytes = message.encode('utf-8')

    signature = hmac.new(secret_key_bytes, message_bytes, hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')

    return signature_b64


# API Views and ViewSets


# Register view
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Logout view (client clears token, but you can log it server-side if you want)
class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully"})

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the UserProfile of the logged-in user
        return self.request.user.userprofile

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ContactMessageCreateAPIView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]


class WishlistViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

        if not created:
            wishlist_item.delete()
            return Response({'status': 'removed', 'detail': 'Product removed from wishlist.'}, status=status.HTTP_200_OK)

        return Response({'status': 'added', 'detail': 'Product added to wishlist.'}, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = WishlistItem.objects.filter(user=request.user).select_related('product')
        serializer = WishlistItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = []  # Adjust as needed

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return Order.objects.all()
        elif user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        order = serializer.save()

        # Handle coupon usage for COD orders
        if order.payment_method == 'cod' and order.coupon_code:
            try:
                coupon = Coupon.objects.get(code=order.coupon_code)
                coupon.increment_usage()
                CouponUsage.objects.create(user=order.user, coupon=coupon, order=order)
            except Coupon.DoesNotExist:
                pass  # optionally log

        # Start payment for online methods
        if order.payment_method == 'khalti':
            payment_url = self.start_khalti_payment(order)
            self.payment_url = payment_url
        elif order.payment_method == 'esewa':
            payment_url = self.start_esewa_payment(order)
            self.payment_url = payment_url
        else:
            self.payment_url = None

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['payment_url'] = getattr(self, 'payment_url', None)
        return response

    def start_khalti_payment(self, order):
        headers = {
            'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        payload = {
            'return_url': settings.KHALTI_RETURN_URL,
            'website_url': settings.SITE_URL,
            'amount': int(order.total_amount * 100),  # Khalti expects paisa
            'purchase_order_id': str(order.id),
            'purchase_order_name': f'Order {order.id}',
            'customer_info': {
                'name': f'{order.first_name} {order.last_name}',
                'email': order.email,
                'phone': order.phone,
            },
        }
        response = requests.post(settings.KHALTI_INITIATE_URL, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            order.payment_id = data.get('pidx')
            order.save()
            return data.get('payment_url')
        return None

    def start_esewa_payment(self, order):
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
        signature = generate_esewa_signature(settings.ESEWA_SECRET_KEY, esewa_data, esewa_data['signed_field_names'].split(','))
        esewa_data['signature'] = signature

        order.payment_id = transaction_uuid
        order.save()

        # Return eSewa payment page URL or data to frontend to redirect or auto-submit
        return settings.ESEWA_PAYMENT_URL  # Frontend must handle posting data to this URL


class EsewaVerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, oid):
        order = get_object_or_404(Order, id=oid)
        refId = request.data.get('refId')
        payment_status = request.data.get('status')  # 'su' or 'failed'

        if not refId or not payment_status:
            return Response({"detail": "refId and status required."}, status=status.HTTP_400_BAD_REQUEST)

        if payment_status == 'su':
            order.status = 'paid'
            order.payment_id = refId
            order.save()

            # Clear session cart logic not applicable to mobile (unless using token-based sessions)
            # Handle coupon usage
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

            return Response({"detail": "Payment verified successfully", "order_id": order.id}, status=status.HTTP_200_OK)

        order.status = 'failed'
        order.save()

class KhaltiVerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pidx = request.data.get('pidx')
        if not pidx:
            return Response({'detail': 'Missing pidx'}, status=drf_status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, payment_id=pidx)

        headers = {
            'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        payload = {'pidx': pidx}

        try:
            response = requests.post(settings.KHALTI_LOOKUP_URL, json=payload, headers=headers)
        except requests.RequestException:
            order.status = 'failed'
            order.save()
            return Response({'detail': 'Failed to contact Khalti server'}, status=drf_status.HTTP_503_SERVICE_UNAVAILABLE)

        if response.status_code == 200:
            data = response.json()
            payment_status = data.get('status')

            if payment_status == 'Completed':
                order.status = 'paid'
                order.save()

                # Handle coupon usage
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

                return Response({'detail': 'Payment verified successfully', 'order_id': order.id}, status=drf_status.HTTP_200_OK)
            
            else:
                order.status = 'failed'
                order.save()
                return Response({'detail': 'Payment verification failed', 'order_id': order.id, 'payment_status': payment_status}, status=drf_status.HTTP_400_BAD_REQUEST)
        else:
            order.status = 'failed'
            order.save()
            return Response({'detail': 'Failed to verify payment with Khalti', 'order_id': order.id}, status=drf_status.HTTP_400_BAD_REQUEST)

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        blog_id = self.request.query_params.get('blog')
        if blog_id:
            return BlogComment.objects.filter(blog_id=blog_id).order_by('-created_at')
        return BlogComment.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [AllowAny]


class NewsletterSubscriberCreateAPIView(generics.CreateAPIView):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [AllowAny]


class CouponApplyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('coupon_code', '').strip()
        cart_total = request.data.get('cart_total')

        if cart_total is None:
            return Response({"detail": "Cart total is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_total = Decimal(cart_total)
        except:
            return Response({"detail": "Invalid cart total."}, status=status.HTTP_400_BAD_REQUEST)

        if cart_total <= 0:
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            return Response({"detail": "Invalid coupon code."}, status=status.HTTP_404_NOT_FOUND)

        # Check if coupon is active
        if not coupon.active:
            return Response({"detail": "This coupon is no longer active."}, status=status.HTTP_400_BAD_REQUEST)

        # Check validity date
        if coupon.valid_until and coupon.valid_until < timezone.now().date():
            return Response({"detail": "This coupon has expired."}, status=status.HTTP_400_BAD_REQUEST)

        # Check usage limit
        if coupon.usage_limit is not None and coupon.times_used >= coupon.usage_limit:
            return Response({"detail": "This coupon has reached its usage limit."}, status=status.HTTP_400_BAD_REQUEST)

        # Check min cart value
        if coupon.min_cart_value is not None and cart_total < coupon.min_cart_value:
            return Response({
                "detail": f"Minimum cart value for this coupon is रु {coupon.min_cart_value}."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already used
        if CouponUsage.objects.filter(user=request.user, coupon=coupon).exists():
            return Response({"detail": "You have already used this coupon."}, status=status.HTTP_400_BAD_REQUEST)

        # Passed all checks
        data = {
            "code": coupon.code,
            "discount": float(coupon.discount),
            "max_discount_amount": float(coupon.max_discount_amount) if coupon.max_discount_amount else None,
        }
        return Response({
            "detail": f"Coupon '{coupon.code}' applied successfully!",
            "coupon": data
        }, status=status.HTTP_200_OK)
    
class FlashSaleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FlashSale.objects.all()
    serializer_class = FlashSaleSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        current_time = now()
        sales = self.get_queryset().filter(start_time__lte=current_time, end_time__gte=current_time)
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)