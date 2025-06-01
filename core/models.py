from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

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
    price = models.DecimalField(max_digits=8, decimal_places=2)
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
    rating = models.FloatField(default=5)  # e.g. 1 to 5 stars
    comment = models.TextField()

    def __str__(self):
        return f"{self.author_name} from {self.author_location}"
    
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

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    notes = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50, default='cod')
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog_images/')
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email