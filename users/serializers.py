from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())],)

    class Meta:
        model = User
        fields = 'id', 'username', 'email', 'password', 'full_name', 'is_superuser'
        read_only_fields = ['is_superuser', 'id']
        extra_kwargs = {'password': {'write_only': True},
                        'username': {'validators': [UniqueValidator(queryset=User.objects.all(), message="A user with that username already exists.")]
                                     }
                        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.set_password(instance.password)
        instance.save()
        return instance