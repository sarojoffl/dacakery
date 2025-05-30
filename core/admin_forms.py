from django import forms
from .models import Slider, AboutSection, BlogCategory
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
