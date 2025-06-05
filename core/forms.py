from django import forms
from .models import ContactMessage, BlogComment

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }

class NewsletterForm(forms.Form):
    email = forms.EmailField(label='Your email', max_length=254)

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }