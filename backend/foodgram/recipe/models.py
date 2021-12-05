from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента', max_length=200, unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Ед. измерения', max_length=30
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта', max_length=200, unique=True
    )
    text = models.TextField(
        verbose_name='Описание рецепта', blank=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeHasIngredient'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return '{}'.format(self.name,)


class RecipeHasIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиенты'
    )
    amount = models.PositiveSmallIntegerField(verbose_name='кол-во')

    class Meta:
        ordering = ['ingredient']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return '{} для {}'.format(self.ingredient, self.recipe)
