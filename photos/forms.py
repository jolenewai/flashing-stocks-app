from django import forms
from .models import Photo, Category, Tag


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = (
            'image',
            'caption',
            'desc',
            'price',
            'tags',
            'category'
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'category-name',
                'required': True,
                'placeholder': 'Enter category name...'
            }),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'tag-name',
                'required': True,
                'placeholder': 'Enter tag name...'
            }),
        }
