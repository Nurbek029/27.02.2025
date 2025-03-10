from django import forms
from .models import Product

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'category',
            'main_images',
            'images',
            'description',
            'price',
        )

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'category',
            'main_images',
            'images',
            'description',
            'price',
        )
