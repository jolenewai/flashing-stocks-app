from django import forms
from .models import Customer
from django.contrib.auth.models import Group
from bootstrap_datepicker_plus import DatePickerInput


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
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
            'dob': DatePickerInput(),
            # default date-format %m/%d/%Y will be used
        }


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    user_type = [
        ('1', 'Customer'),
        ('2', 'Photographer'),
    ]
    sign_up_as = forms.ChoiceField(required=True, choices=user_type)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        if self.cleaned_data['sign_up_as'] == '1':
            customer_group = Group.objects.get(name="customers")
            customer_group.user_set.add(user)
        else:
            photographer_group = Group.objects.get(name="photographers")
            photographer_group.user_set.add(user)
