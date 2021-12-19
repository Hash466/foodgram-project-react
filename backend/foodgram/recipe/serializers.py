from rest_framework import serializers

from .models import (
    Ingredient, Tag, Recipe, RecipeHasIngredient, RecipeHasTag
)
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_amount(self, obj):
        return RecipeHasIngredient.objects.filter(
            ingredient=obj.pk,
            recipe=obj.pk__ingredients__recipe__ingredients
        )
        # return RecipeHasIngredient.objects.get(ingredient=obj.pk).amount
        # obj.ingredients.values(). -> QuerySet


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientForRecipeSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name',
            'image', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags['tags']:
            current_tag, status = Tag.objects.get_or_create(pk=tag)
            RecipeHasTag.objects.create(
                recipe=recipe, tag=current_tag)

        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                pk=ingredient['id']
            )
            current_amount = ingredient.get('amount')
            RecipeHasIngredient.objects.create(
                recipe=recipe, ingredient=current_ingredient,
                amount=current_amount
            )

        return recipe
