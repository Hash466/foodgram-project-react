from django.contrib import admin

from .models import Ingredient, Recipe, Tag

EMPTY_VALUE = '-пусто-'


class RecipeHasIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeHasTagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


class FavoriteHasRecipeInline(admin.TabularInline):
    model = Recipe.favorites.through
    extra = 1


class UserHasShoppingCartInline(admin.TabularInline):
    model = Recipe.shopping_cart.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'cooking_time'
    )
    search_fields = ('name',)
    list_filter = ('cooking_time',)
    empty_value_display = EMPTY_VALUE
    inlines = (
        RecipeHasIngredientInline, RecipeHasTagInline, FavoriteHasRecipeInline,
        UserHasShoppingCartInline
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
