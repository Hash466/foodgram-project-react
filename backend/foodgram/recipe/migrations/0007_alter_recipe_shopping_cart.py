# Generated by Django 3.2 on 2021-12-21 20:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0006_auto_20211221_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='shopping_cart',
            field=models.ManyToManyField(related_name='shopping_carts', through='recipe.UserHasShoppingCart', to=settings.AUTH_USER_MODEL),
        ),
    ]
