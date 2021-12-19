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
        User, verbose_name="Автор рецепта",
        on_delete=models.CASCADE, related_name="recipes"
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
        upload_to='static/images/', blank=True, null=True,
        verbose_name="Картинка"
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

    def __str__(self):
        return '{} для {}'.format(self.tag, self.recipe)


class RecipeHasIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиенты'
    )
    amount = models.PositiveSmallIntegerField(verbose_name='кол-во')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return '{} для {}'.format(self.ingredient, self.recipe)
