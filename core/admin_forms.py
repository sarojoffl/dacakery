from django import forms
from .models import (
    Slider, AboutSection, BlogCategory, BlogPost, Testimonial, InstagramSection,
    InstagramImage, Category, Product, Coupon
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ckeditor.widgets import CKEditorWidget

class AdminSliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['title', 'image', 'button_text']

class AboutSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = [
            'title', 'heading', 'description',
            'cakes_baked', 'cakes_delivered',
            'happy_customers', 'years_of_baking'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author', 'image', 'category']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['author_name', 'author_location', 'author_image', 'rating', 'comment']

class InstagramSectionForm(forms.ModelForm):
    class Meta:
        model = InstagramSection
        fields = ['heading', 'subheading', 'instagram_handle']

class InstagramImageForm(forms.ModelForm):
    class Meta:
        model = InstagramImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon_class']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'in_stock', 'tags', 'price', 'image']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'active']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep the current password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return make_password(password)
        else:
            # Password not changed
            return self.instance.password