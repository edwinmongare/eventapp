from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    
    First_name = forms.CharField(required=True)
    Second_name = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=12)
    # shipping_country = CountryField(blank_label='Countries').formfield(
    #     required=False,
    #     widget=CountrySelectWidget(attrs={
    #         'class': 'w-100',
            
    #     }))
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class SeachForm(forms.Form):
    result = forms.CharField(required=True)

    