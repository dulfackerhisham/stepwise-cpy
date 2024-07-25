from django import forms
from . models import Product_Review

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))

    class Meta:
        model = Product_Review
        fields = ['review', 'rating']