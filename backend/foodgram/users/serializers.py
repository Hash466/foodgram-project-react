from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name'
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
