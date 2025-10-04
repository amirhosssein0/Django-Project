from django import forms
from .models import ShipingAddress
from phonenumber_field.formfields import PhoneNumberField

class ShipingForm(forms.ModelForm):
    shiping_full_name = forms.CharField(
    widget=forms.TextInput(attrs={
        'placeholder':'Full Name'
        
    }),
    required=True
    )
    shiping_phone = PhoneNumberField(
    widget=forms.TextInput(attrs={
        'placeholder':'phone number'
    }),
    region='US',
    required=True
    )
    shiping_address = forms.CharField(
    widget=forms.TextInput(attrs={
        'placeholder':'address'
    }),
    required=True
    )

    
    class Meta:
        model = ShipingAddress
        fields = ['shiping_full_name', 'shiping_phone', 'shiping_address']
        exclude = ('user',)
