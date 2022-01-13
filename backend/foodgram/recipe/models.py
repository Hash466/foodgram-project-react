from colorfield.fields import ColorField
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента', max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Ед. измерения', max_length=200
    )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега', max_length=200
    )
    color = ColorField(
        verbose_name='HEX-код', default='#FF0000'
    )
    slug = models.SlugField(
        verbose_name='slug', max_length=200
    )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return '{}'.format(self.name,)


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта', max_length=200, unique=True
    )
    author = models.ForeignKey(
        User, verbose_name='Автор рецепта',
        on_delete=models.CASCADE, related_name='recipes'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeHasIngredient'
    )
    tags = models.ManyToManyField(
        Tag, through='RecipeHasTag'
    )
    image = models.ImageField(
        upload_to='media/images/', blank=True, null=True,
        verbose_name='Картинка'
    )
    favorites = models.ManyToManyField(
        User, through='FavoriteHasRecipe', related_name='favorites'
    )
    shopping_cart = models.ManyToManyField(
        User, through='UserHasShoppingCart', related_name='shopping_carts'
    )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return '{}'.format(self.name,)


class RecipeHasTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, verbose_name='Теги'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique tag value'
            ),
        )

    def __str__(self):
        return 'Тег {} у рецепта {}'.format(self.tag, self.recipe)


class RecipeHasIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиенты'
    )
    amount = models.PositiveSmallIntegerField(verbose_name='кол-во')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient value'
            ),
        )

    def __str__(self):
        return 'Ингредиент {} для рецепта {}'.format(
            self.ingredient, self.recipe
        )


class FavoriteHasRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователи'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='in_favorite'
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favorite value'
            ),
        )

    def __str__(self):
        return 'Рецепт {} в избранном у {}'.format(self.recipe, self.user)


class UserHasShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователи',
        related_name='carts_user'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='carts',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique shopping cart value'
            ),
        )

    def __str__(self):
        return 'Рецепт {} в списке покупок у {}'.format(self.recipe, self.user)
