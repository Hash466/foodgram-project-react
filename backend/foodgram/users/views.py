from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .models import User
from .serializers import UserSerializer


class CreateListRetrieveViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def me(self, request):
        user = User.objects.get_object_or_404(username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    # @action(methods=['post'], detail=True)
    # def set_password(self, request):
    #     user = User.objects.get(username=request.username)
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data)
