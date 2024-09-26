''' User Authentication Serializer File '''
import logging
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import ValidationError
from user_authentication.models import User,UserDetails


logger = logging.getLogger(__name__)
class UserDetailsSerializer(serializers.ModelSerializer):
    ''' UserDetails Serializer '''
    username = serializers.SerializerMethodField(read_only=True)
    user_full_name = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    
    def get_username(self, obj):
        ''' Get User Name '''
        username = None
        try:
            username = obj.user.username
        except Exception as exp:
            logger.exception(exp)
        return username

    def get_user_full_name(self, obj):
        ''' Get User Type Name '''
        user_full_name = None
        try:
            user_full_name = obj.user.get_full_name()
        except Exception as exp:
            logger.exception(exp)
        return user_full_name

    def get_first_name(self, obj):
        ''' Get User Type Name '''
        first_name = None
        try:
            first_name = obj.user.first_name
        except Exception as exp:
            logger.exception(exp)
        return first_name

    def get_last_name(self, obj):
        ''' Get User Type Name '''
        last_name = None
        try:
            last_name = obj.user.last_name
        except Exception as exp:
            logger.exception(exp)
        return last_name

    def get_email(self, obj):
        ''' Get User Type Name '''
        email = None
        try:
            email = obj.user.email
        except Exception as exp:
            logger.exception(exp)
        return email

 
    class Meta:
        ''' Meta Class '''
        model = UserDetails
        fields = '__all__'

class LoginSerializer(TokenObtainPairSerializer):
    ''' Login Serializer '''
    username = serializers.CharField(
        max_length=255, min_length=5, allow_blank=False)
    password = serializers.CharField(
        max_length=40, min_length=8, allow_blank=False)

    def validate(self, attrs):
        ''' Validate '''
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['id'] = self.user.pk
        return data

class UserTokenVerifySerializer(TokenVerifySerializer):
    ''' UserTokenVerifySerializer '''
    token = serializers.CharField(max_length=255, allow_blank=False)

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            print(data)
            print(self.user.username)
            return data
        except TokenError:
            raise TokenError('bad_token')

class SignUpSerializer(serializers.Serializer):
    ''' Sign Up Serializer '''
    username = serializers.CharField(
        max_length=255, min_length=5, allow_blank=False)
    password = serializers.CharField(
        max_length=150, min_length=8, allow_blank=False)
    confirm_password = serializers.CharField(
        max_length=150, min_length=8, allow_blank=False)
    email = serializers.EmailField(
        max_length=150, allow_blank=False)
    first_name = serializers.CharField(
        max_length=150, allow_blank=False)
    last_name = serializers.CharField(
        max_length=150, allow_blank=False)
    phone = serializers.CharField(
        max_length=150, min_length=8, allow_blank=False)


    def validate(self, data):
        # Retrieve the password and confirm_password fields from the data
        user_obj = User.objects.filter(username=data.get('username'))
        if user_obj.exists():
            raise ValidationError("User already exists")
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("User email already exists")

        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Check if the passwords match
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return data

