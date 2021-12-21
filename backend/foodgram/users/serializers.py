from djoser.serializers import SetPasswordSerializer as DjSetPasswordSerializer
from djoser.serializers import UserCreateSerializer as DjUserCreateSerializer
from rest_framework import serializers

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
