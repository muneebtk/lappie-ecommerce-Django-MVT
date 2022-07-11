from django import forms
from category.models import Category
from orders.models import Order
from user.models import user

from store.models import FeaturedProduct, Product, Variation,Coupons,HomeCarousel


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class AdminForm(forms.Form):
    class Meta:
        model = user
        fields = ['email','password']
    
    email = forms.EmailField(widget = forms.EmailInput(attrs={
        'class':'form-control',
        }))
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'class':'form-control',
        }))

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = '__all__'

class FeaturedProductForm(forms.ModelForm):
    
    class Meta:
        model = FeaturedProduct
        fields = '__all__'
class CouponsForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = '__all__'

class HomeCarouselForm(forms.ModelForm):
    class Meta:
        model = HomeCarousel
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['status']


