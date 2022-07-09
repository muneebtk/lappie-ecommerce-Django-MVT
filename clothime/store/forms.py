from django import forms
from orders .models import Address 

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city','pincode',]