from django import forms
from .models import Photographer
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class META:
        model = User
        fields = ('first_name', 'last_name')


class PhotographerForm(forms.ModelForm):
    class META:
        model: Photographer
        fields = (
            'display_name',
            'dob',
            'address_line1',
            'address_line2',
            'postal_code',
            'city',
            'country',
            'country_code',
            'contact_number'
        )