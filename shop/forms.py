from django import forms
from .models import Product, Rating, Cart, Order
from django. contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating' 'comment')
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        
        
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'postal_code', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }