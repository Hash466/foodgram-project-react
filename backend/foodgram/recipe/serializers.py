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
        fields = ('id', 'name', 'measurement_unit')


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id', read_only=True)
    name = serializers.ReadOnlyField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeHasIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name',
            'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = RecipeHasIngredient.objects.filter(recipe=obj)
        return IngredientForRecipeSerializer(ingredients, many=True).data

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
