from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from foodgram.settings import CUSTOM_SETTINGS_DRF

from .filters import RecipeFilter
from .models import (FavoriteHasRecipe, Ingredient, Recipe,
                     RecipeHasIngredient, Tag, UserHasShoppingCart)
from .permissions import IsAuthorOrAdmin
from .serializers import (IngredientSerializer, RecipeForFavoriteSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


class RecipeSetPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = CUSTOM_SETTINGS_DRF.get('PAGE_SIZE_RECIPE')


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
    pagination_class = RecipeSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrAdmin,)

    def get_serializer_class(self):
        if self.action == 'favorite':
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

    @action(
        ['post', 'delete'], detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
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


class ShoppingCartView(APIView):
    http_method_names = ['post', 'delete']
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = ShoppingCartSerializer(
            data={'user': user.id, 'recipe': recipe.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(recipe=recipe, user=request.user)
        serializer = RecipeForFavoriteSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        cart = get_object_or_404(
            UserHasShoppingCart, user=user, recipe__id=recipe_id
        )
        cart.delete()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_shopping_cart(request):
    user = request.user
    cart = UserHasShoppingCart.objects.filter(user=user)
    shopping_list = {}
    for item in cart:
        recipe = item.recipe
        ingredients = RecipeHasIngredient.objects.filter(recipe=recipe)
        for item in ingredients:
            amount = item.amount
            name = item.ingredient.name
            measurement_unit = item.ingredient.measurement_unit
            if name in shopping_list:
                shopping_list[name][0] += int(amount)
            else:
                shopping_list[name] = [int(amount), measurement_unit]
    shopping_cart = []
    for item in shopping_list:
        shopping_cart.append(
            f'{item} ({shopping_list[item][1]}) - {shopping_list[item][0]}\n'
        )
    response = HttpResponse(shopping_cart, 'Content-Type: text/plain')
    response['Content-Disposition'] = (
        'attachment;' 'filename="shopping_cart.txt"'
    )

    return response
