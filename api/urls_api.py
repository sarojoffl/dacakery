from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views_api import (
    ProductViewSet,
    OrderViewSet,
    BlogPostViewSet,
    CommentViewSet,
    CouponViewSet,
    CategoryViewSet,
    WishlistViewSet,
    NewsletterSubscriberCreateAPIView,
    ContactMessageCreateAPIView,
    UserProfileAPIView,
    EsewaVerifyAPIView,
    KhaltiVerifyAPIView,
    CouponApplyAPIView,
    RegisterAPIView,
    LogoutAPIView,
    FlashSaleViewSet
)

# DRF router
router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('orders', OrderViewSet, basename='order')
router.register('blogs', BlogPostViewSet, basename='blog')
router.register('comments', CommentViewSet, basename='comment')
router.register('coupons', CouponViewSet, basename='coupon')
router.register('categories', CategoryViewSet, basename='category')
router.register('wishlist', WishlistViewSet, basename='wishlist')
router.register('flashsales', FlashSaleViewSet, basename='flashsale')

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterAPIView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth_logout'),
    
    # User profile
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),

    # Orders + payments
    path('orders/khalti-verify/', KhaltiVerifyAPIView.as_view(), name='khalti_verify'),
    path('orders/esewa-verify/<int:oid>/', EsewaVerifyAPIView.as_view(), name='esewa_verify'),

    # Coupon
    path('coupons/apply/', CouponApplyAPIView.as_view(), name='coupon_apply'),

    # Other custom endpoints
    path('newsletter/', NewsletterSubscriberCreateAPIView.as_view(), name='newsletter_subscribe'),
    path('contact/', ContactMessageCreateAPIView.as_view(), name='contact_message'),

    # Router endpoints (products, orders, blogs, etc.)
    path('', include(router.urls)),
]
