from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('As senha não coincidem.')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)

        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            user = authenticate(username=email_or_username, password=password)
            if not user:
                try:
                    user_obj = User.objects.get(username=email_or_username)
                    user = authenticate(username=user_obj.email, password=password)
                except User.DoesNotExist:
                    pass
            
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')

            if not user.is_active:
                raise serializers.ValidationError('Conta desativada.')

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email/username e senha são obrigatórios.')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'profile_picture', 'bio', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined')

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError('Este nome de usuário já esta em uso.')
        return value

