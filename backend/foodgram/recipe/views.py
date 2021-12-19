from rest_framework import filters, viewsets

from .models import Ingredient, Tag, Recipe
from .serializers import (
    IngredientSerializer, TagSerializer, RecipeSerializer,
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
    serializer_class = RecipeSerializer

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return RecipeCreateSerializer
    #     else:
    #         return RecipeSerializer

    def perform_create(self, serializer):
        # print('\n\n\n*****************************************************')
        # print({'tags': (self.request.data['tags'])})
        # print('*****************************************************\n\n\n')
        serializer.save(
            author=self.request.user,
            tags={'tags': (self.request.data['tags'])},
            ingredients=self.request.data['ingredients'],
        )
