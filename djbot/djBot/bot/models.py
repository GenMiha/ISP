from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(verbose_name='Name', max_length=40)
    price = models.IntegerField(verbose_name='Price')
    description = models.CharField(verbose_name='Description', max_length=255)
    amount = models.IntegerField(verbose_name='Amount', validators=[MinValueValidator(0)])


class User(AbstractUser):
    shipping_address = models.CharField(verbose_name='Shipping address', max_length=255, blank=True, null=True)
    items = models.ManyToManyField(Item)


class UserRating(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(
        verbose_name='Rating',
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )


class CreditCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_number = models.CharField(
        verbose_name='Card Number',
        validators=[RegexValidator(regex=r'^\d{16}$', message='Length has to be 16', code='nomatch')],
        max_length=16
    )
    card_holder_name = models.CharField(verbose_name='Card Holder Name', max_length=35,)
    expiration_month = models.IntegerField(
        verbose_name='Expiration Month',
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    expiration_year = models.IntegerField(
        verbose_name='Expiration Year',
        validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    cvv_number = models.CharField(
        verbose_name='CVV Number',
        validators=[RegexValidator(regex=r'^\d{3}$', message='Length has to be 3', code='nomatch')],
        max_length=3
    )


class Order(models.Model):
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_amount = models.IntegerField(verbose_name='Item Amount', validators=[MinValueValidator(1)])
    total_price = models.IntegerField(verbose_name='Total Price')
