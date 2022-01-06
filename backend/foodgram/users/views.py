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
    # serializer_class = UserSerializer
    pagination_class = UserSetPagination

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif (
            self.action == 'subscriptions' or self.action == 'subscribe'
        ):
            return SubscriptionsSerializer
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

    @action(detail=False)
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(['post', 'delete'], detail=True)
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            Subscription.objects.get_or_create(
                user=user, author=author
            )
            subscribe = Subscription.objects.filter(author=author, user=user)
            serializer = self.get_serializer(subscribe, many=True)
            return Response(serializer.data)
        else:
            subscribe = Subscription.objects.filter(author=author, user=user)
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
