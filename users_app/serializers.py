from rest_framework.serializers import ModelSerializer
from .models import User
from .services import watermark_photo


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'first_name', 'last_name', 'gender', 'photo', 'email']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.gender = validated_data['gender']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.photo = validated_data['photo']
        user.set_password(validated_data["password"])
        user.email = validated_data['email']
        user.save()
        watermark_photo(str(user.photo))
        return user
