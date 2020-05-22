from django import forms
from .models import Photographer
from bootstrap_datepicker_plus import DatePickerInput
from pyuploadcare.dj.forms import ImageField

class PhotographerForm(forms.ModelForm):
    class Meta:
        model = Photographer
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

        widgets = {
            'dob': DatePickerInput(), # default date-format %m/%d/%Y will be used
        }


class AvatarForm(forms.ModelForm):
    profile_img = ImageField(label='', required=False)
    class Meta:
        model = Photographer
        fields = ('profile_img',)



