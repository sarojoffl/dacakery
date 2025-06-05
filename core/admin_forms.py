from django import forms
from .models import (
    Slider, AboutSection, BlogCategory, BlogPost, Testimonial, InstagramSection,
    InstagramImage, Category, Product, Coupon, TeamMember, MapLocation, ContactDetail,
    SpecialOffer, OrganizationDetails, UserProfile, Order
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
        fields = ['name']

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

class SpecialOfferForm(forms.ModelForm):
    class Meta:
        model = SpecialOffer
        fields = ['title', 'description', 'image', 'valid_until', 'coupon']
        widgets = {
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }

class OrganizationDetailsForm(forms.ModelForm):
    class Meta:
        model = OrganizationDetails
        fields = '__all__' 

class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'delivery_date', 'delivery_time',
                  'first_name', 'last_name', 'email', 'phone',
                  'address_line1', 'address_line2', 'city', 'state', 'zip', 'country']
