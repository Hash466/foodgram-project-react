from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .models import (
    Ingredient, Tag, Recipe, FavoriteHasRecipe, UserHasShoppingCart
)
from .serializers import (
    IngredientSerializer, TagSerializer, RecipeSerializer,
    RecipeForFavoriteSerializer
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    #serializer_class = RecipeSerializer ###### ПРОВЕРЬ!

    def get_serializer_class(self):
        if self.action == 'favorite' or self.action == 'shopping_cart':
            return RecipeForFavoriteSerializer
        else:
            return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            tags={'tags': (self.request.data['tags'])},
            ingredients=self.request.data['ingredients'],
        )

    def perform_update(self, serializer):
        recipe = self.get_object()
        serializer.save(
            instance=recipe,
            author=self.request.user,
            tags={'tags': (self.request.data['tags'])},
            ingredients=self.request.data['ingredients'],
        )

    @action(['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            FavoriteHasRecipe.objects.get_or_create(
                user=user, recipe=recipe
            )
            serializer = self.get_serializer(recipe)
            return Response(serializer.data)
        else:
            favorite = FavoriteHasRecipe.objects.filter(
                user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            UserHasShoppingCart.objects.get_or_create(
                user=user, recipe=recipe
            )
            serializer = self.get_serializer(recipe)
            return Response(serializer.data)
        else:
            favorite = UserHasShoppingCart.objects.filter(
                user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
