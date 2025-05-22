from django.db import models
from django.utils.text import slugify

class Slider(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hero/')
    button_text = models.CharField(max_length=100, default="Our cakes")

    def __str__(self):
        return self.title
    
class AboutSection(models.Model):
    title = models.CharField(max_length=255, default="About Cake shop")
    heading = models.CharField(max_length=255, default="Cakes and bakes from the house of Queens!")
    description = models.TextField()

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100)
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