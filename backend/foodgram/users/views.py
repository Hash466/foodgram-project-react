from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from foodgram.settings import CUSTOM_SETTINGS_DRF

from .models import User, Subscription
from .serializers import (SetPasswordSerializer, UserCreateSerializer,
                          UserSerializer, SubscriptionsSerializer)


class CreateListRetrieveViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class UserSetPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = CUSTOM_SETTINGS_DRF.get('PAGE_SIZE_USERS')


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserSetPagination

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        else:
            return UserSerializer

    @action(detail=False)
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(['post'], detail=False)
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(ListViewSet):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user)


class SubscribeViewSet(CreateDestroyViewSet):
    serializer_class = SubscriptionsSerializer
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        print('\n\n\n********************************************')
        print(self.kwargs['id'])
        print(self.http_method_names)
        print('********************************************\n\n\n')
        serializer.save(
            user=self.request.user,
            author=get_object_or_404(User, id=self.kwargs['id'])
        )

    def perform_destroy(self, instance):
        print('\n\n\n********************************************')
        print(self.kwargs['id'])
        print(self.http_method_names)
        print('********************************************\n\n\n')
        instance.delete()

    # def destroy(self, request, *args, **kwargs):
    #     instance = get_object_or_404(
    #         Subscription,
    #         user=self.request.user,
    #         author=User.objects.get(id=self.kwargs['id'])
    #     )
    #     print('\n\n\n********************************************')
    #     print(instance)
    #     print('********************************************\n\n\n')
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
