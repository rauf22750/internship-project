# forms.py
from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['review_text', 'review_rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
            'review_rating': forms.Select(choices=ProductReview._meta.get_field('review_rating').choices)
        }
