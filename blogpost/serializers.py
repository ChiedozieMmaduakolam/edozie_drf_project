from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser, OneTimePassword, BlogPost, Comments
from django.contrib.auth.password_validation import validate_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # if not self.user.is_verified:
        #     raise AuthenticationFailed('This email is not verified yet')

        # Add extra user data (optional)
        data['username'] = self.user.username
        data['email'] = self.user.email

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'confirm_password', 'cover_photo')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            cover_photo=validated_data['cover_photo']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class VerifyEmailSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(min_length=6, max_length=10, write_only=True)

    class Meta:
        model = OneTimePassword
        fields = ['otp_code']

# class ProfileSerializer(serializers.ModelSerializer):
#     #notes = NoteSerializer(many=True, read_only=True)

#     class Meta:
#         model = CustomUser
#         fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'commenter', 'comment', 'date_posted']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(read_only=True, slug_field='id')
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'date_posted', 'author', 'comments']