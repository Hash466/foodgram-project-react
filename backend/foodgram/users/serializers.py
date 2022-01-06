from djoser.serializers import SetPasswordSerializer as DjSetPasswordSerializer
from djoser.serializers import UserCreateSerializer as DjUserCreateSerializer
from rest_framework import serializers

from recipe.models import Recipe

from .models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        subscribed = Subscription.objects.filter(author__following__user=obj)
        return bool(subscribed)


class UserCreateSerializer(DjUserCreateSerializer):
    pass


class SetPasswordSerializer(DjSetPasswordSerializer):
    pass


class RecipeForSubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    # def get_name(self, obj):
    #     print('\n\n\n********************************************')
    #     print('user')
    #     print(user.username)
    #     print(Subscription.objects.filter(user=user))
    #     print('********************************************\n\n\n')
    #     return obj


class SubscriptionsSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email', read_only=True)
    id = serializers.ReadOnlyField(source='author.id', read_only=True)
    username = serializers.ReadOnlyField(
        source='author.username', read_only=True
    )
    first_name = serializers.ReadOnlyField(
        source='author.first_name', read_only=True
    )
    last_name = serializers.ReadOnlyField(
        source='author.last_name', read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.author)
        return RecipeForSubscriptionsSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj.author).count()
        return recipes
