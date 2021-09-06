from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from bot.models import CreditCard, User


class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ('card_number', 'card_holder_name', 'expiration_month', 'expiration_year', 'cvv_number')


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'shipping_address')


