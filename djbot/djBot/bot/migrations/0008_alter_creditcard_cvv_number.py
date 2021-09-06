# Generated by Django 3.2.7 on 2021-09-05 13:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_alter_creditcard_cvv_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='cvv_number',
            field=models.IntegerField(max_length=3, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 3', regex='^\\d{3}$')], verbose_name='CVV Number'),
        ),
    ]
