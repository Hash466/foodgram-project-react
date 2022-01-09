# Generated by Django 3.2 on 2021-12-20 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20211219_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipehasingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipehasingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe'),
        ),
    ]
