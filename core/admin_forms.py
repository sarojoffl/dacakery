from django import forms
from .models import Slider, AboutSection, BlogCategory, BlogPost, Testimonial, InstagramSection, InstagramImage
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