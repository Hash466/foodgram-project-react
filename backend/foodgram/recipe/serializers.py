from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from users.serializers import UserSerializer
from .models import (
    FavoriteHasRecipe, Ingredient, Recipe,RecipeHasIngredient, RecipeHasTag,
    Tag, UserHasShoppingCart
)


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
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name',
            'image', 'text', 'cooking_time', 'is_favorited',
            'is_in_shopping_cart'
        )

    def get_ingredients(self, obj):
        ingredients = RecipeHasIngredient.objects.filter(recipe=obj)
        return IngredientForRecipeSerializer(ingredients, many=True).data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags['tags']:
            current_tag = get_object_or_404(Tag, pk=tag)
            RecipeHasTag.objects.get_or_create(
                recipe=recipe, tag=current_tag)

        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, pk=ingredient['id']
            )
            current_amount = ingredient.get('amount')
            if int(current_amount) < 1:
                raise serializers.ValidationError(
                    "Количество единиц ингредиента не может быть меньше 1"
                )
            RecipeHasIngredient.objects.get_or_create(
                recipe=recipe, ingredient=current_ingredient,
                amount=current_amount
            )

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.filter(pk=instance.id)
        instance = validated_data.pop('instance')
        recipe.update(**validated_data)

        old_inst_tags = [item[0] for item in instance.tags.values_list('id')]
        old_inst_ingredients = [
            item[0] for item in instance.ingredients.values_list('id')
        ]

        for tag in tags['tags']:
            current_tag = get_object_or_404(Tag, pk=tag)
            if current_tag.pk in old_inst_tags:
                old_inst_tags.remove(current_tag.pk)
            else:
                RecipeHasTag.objects.get_or_create(
                    recipe=instance, tag=current_tag
                )
        for tag_id in old_inst_tags:
            del_tag = RecipeHasTag.objects.filter(
                recipe=instance.id, tag=tag_id
            )
            del_tag.delete()

        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, pk=ingredient['id']
            )
            if current_ingredient.pk in old_inst_ingredients:
                old_inst_ingredients.remove(current_ingredient.pk)
            else:
                current_amount = ingredient.get('amount')
                if int(current_amount) < 1:
                    raise serializers.ValidationError(
                        "Количество единиц ингредиента не может быть меньше 1"
                    )
                RecipeHasIngredient.objects.get_or_create(
                    recipe=instance, ingredient=current_ingredient,
                    amount=current_amount
                )
        for ingredient_id in old_inst_ingredients:
            del_ingredient = RecipeHasIngredient.objects.filter(
                recipe=instance.id, ingredient=ingredient_id
            )
            del_ingredient.delete()

        return instance

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return FavoriteHasRecipe.objects.filter(
            recipe=obj, user=request.user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return UserHasShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()
    

class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    recipe = serializers.IntegerField(source='recipe.id')

    class Meta:
        model = UserHasShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']['id']
        recipe = data['recipe']['id']
        if UserHasShoppingCart.objects.filter(
            user=user, recipe__id=recipe
        ).exists():
            raise serializers.ValidationError(
                {
                    "errors": "Вы уже добавили рецепт в корзину"
                }
            )
        return data


class RecipeForFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
