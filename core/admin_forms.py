from django import forms
from .models import (
    Slider, AboutSection, BlogCategory, BlogPost, Testimonial, InstagramSection,
    InstagramImage, Category, Product, ProductImage, Coupon, TeamMember, MapLocation, ContactDetail,
    FlashSale, OrganizationDetails, UserProfile, Order,ProductOption, ProductOptionPrice,
    FlashSaleItem
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
    content = forms.CharField(widget=CKEditorWidget())

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
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'in_stock', 'tags', 'price', 'image']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']

class ProductOptionForm(forms.ModelForm):
    class Meta:
        model = ProductOption
        fields = ['name', 'type', 'default_price']

class ProductOptionPriceForm(forms.ModelForm):
    class Meta:
        model = ProductOptionPrice
        fields = ['product', 'option', 'price']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            'code', 
            'discount', 
            'max_discount_amount', 
            'min_cart_value',
            'usage_limit',
            'valid_until', 
            'active'
        ]
        widgets = {
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }

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
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'image', 'facebook', 'twitter', 'instagram', 'youtube']

class MapLocationForm(forms.ModelForm):
    class Meta:
        model = MapLocation
        fields = '__all__'

class ContactDetailForm(forms.ModelForm):
    class Meta:
        model = ContactDetail
        fields = '__all__'


class FlashSaleForm(forms.ModelForm):
    class Meta:
        model = FlashSale
        fields = ['title', 'start_time', 'end_time', 'banner_image', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(FlashSaleForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['banner_image'].widget.attrs['class'] = 'form-control-file'

class FlashSaleItemForm(forms.ModelForm):
    class Meta:
        model = FlashSaleItem
        fields = ['flash_sale', 'product', 'discounted_price']
        widgets = {
            'discounted_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super(FlashSaleItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class OrganizationDetailsForm(forms.ModelForm):
    class Meta:
        model = OrganizationDetails
        fields = '__all__' 

class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'delivery_date', 'delivery_time',
                  'first_name', 'last_name', 'email', 'phone',
                  'address', 'address_line2', 'city', 'province', 'postal_code']
