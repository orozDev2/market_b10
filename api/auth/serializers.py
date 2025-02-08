from rest_framework import serializers

from account.services import User


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'avatar',
            'phone',
            'first_name',
            'last_name',
            'email',
            'role',
        )