from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.timezone import now


# -------------------------
# User & Profile
# -------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# -------------------------
# Home Page Content
# -------------------------
class Slider(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hero/')
    button_text = models.CharField(max_length=100, default="Our cakes")

    def __str__(self):
        return self.title


class AboutSection(models.Model):
    title = models.CharField(max_length=255, default="About Cake Shop")
    heading = models.CharField(max_length=255, default="Cakes and bakes from the house of Queens!")
    description = models.TextField()
    cakes_baked = models.PositiveIntegerField(default=0)
    cakes_delivered = models.PositiveIntegerField(default=0)
    happy_customers = models.PositiveIntegerField(default=0)
    years_of_baking = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


# -------------------------
# Product & Categories
# -------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    in_stock = models.BooleanField(default=True)
    tags = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # base price
    image = models.ImageField(upload_to='products/')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductOption(models.Model):
    OPTION_TYPES = (
        ('size', 'Size'),
        ('extra', 'Extra'),
    )

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=OPTION_TYPES)
    default_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ('name', 'type')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class ProductOptionPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='option_prices')
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # option price for this product

    class Meta:
        unique_together = ('product', 'option')

    def __str__(self):
        return f"{self.product.name} - {self.option.name}: Rs. {self.price}"


# -------------------------
# Team & Testimonials
# -------------------------
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    author_location = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='testimonial/')
    rating = models.FloatField(default=5)
    comment = models.TextField()

    def __str__(self):
        return f"{self.author_name} from {self.author_location}"


# -------------------------
# Instagram Section
# -------------------------
class InstagramSection(models.Model):
    heading = models.CharField(max_length=100)
    subheading = models.CharField(max_length=255)
    instagram_handle = models.CharField(max_length=100)

    def __str__(self):
        return self.instagram_handle


class InstagramImage(models.Model):
    section = models.ForeignKey(InstagramSection, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='instagram/')

    def __str__(self):
        return f"Image for {self.section.instagram_handle}"


# -------------------------
# Contact & Location
# -------------------------
class MapLocation(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    map_iframe = models.TextField()

    def __str__(self):
        return self.title


class ContactDetail(models.Model):
    title = models.CharField(max_length=100, default="Contact With us")
    availability_note = models.CharField(max_length=255, default="Representatives or Advisors are available:")
    weekday_hours = models.CharField(max_length=100, default="Mon-Fri: 5:00am to 9:00pm")
    weekend_hours = models.CharField(max_length=100, default="Sat-Sun: 6:00am to 9:00pm")
    image = models.ImageField(upload_to='contact/', null=True, blank=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


# -------------------------
# Wishlist
# -------------------------
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


# -------------------------
# Orders
# -------------------------
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    notes = models.TextField(blank=True)

    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('khalti', 'Khalti'),
        ('esewa', 'eSewa'),
    ]
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cod')

    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('failed', 'Payment Failed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    eggless = models.BooleanField(default=False)
    sugarless = models.BooleanField(default=False)
    size = models.CharField(max_length=20, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)

    def get_subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# -------------------------
# Coupons & Offers
# -------------------------
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class SpecialOffer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='offers/')
    valid_until = models.DateField(null=True, blank=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    def is_active(self):
        return self.valid_until >= now().date() if self.valid_until else True

    def __str__(self):
        return self.title


# -------------------------
# Blog
# -------------------------
class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    image = models.ImageField(upload_to='blog_images/')
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.get_full_name or self.user.username} on {self.blog.title}"


# -------------------------
# Newsletter
# -------------------------
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# -------------------------
# Organization Info
# -------------------------
class OrganizationDetails(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    working_hours_mon_fri = models.CharField(max_length=50, default="08:00 am – 08:30 pm")
    working_hours_sat = models.CharField(max_length=50, default="10:00 am – 16:30 pm")
    working_hours_sun = models.CharField(max_length=50, default="10:00 am – 16:30 pm")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter URL")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram URL")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube URL")

    def __str__(self):
        return self.name
