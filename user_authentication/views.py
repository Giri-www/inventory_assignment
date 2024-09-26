from django.shortcuts import render

# Create your views here.
''' User Authentication Views File '''
import logging
import math
from copy import deepcopy
from django.db.models import Q
from django.db import transaction
from django.db import connection
from django.db.models.functions import Concat
from django.db.models import Value, CharField
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin, CreateModelMixin)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from user_authentication.models import UserDetails, User
from user_authentication.serializers import (
    LoginSerializer,UserDetailsSerializer, UserTokenVerifySerializer,  SignUpSerializer,  UserUpdateSerializer)
from django.conf import settings
from .utils import serializer_error_format

# Create your views here.
logger = logging.getLogger(__name__)


class Login(TokenObtainPairView):
    ''' User Login '''
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        ''' User Login '''
        serializer = LoginSerializer()
        login_response = {}
        http_status = None
        user = authenticate(
            username=request.data['username'], password=request.data['password'])
        logger.info("User : %s", user)
        if user:
            logger.info("Valid User")
            serializer_data = serializer.validate(attrs=request.data)
            logger.info("Serializer Data : %s ", serializer_data)
            user_details_obj = UserDetails.objects.get(
                user_id=serializer_data['id'])
            user_details_data = UserDetailsSerializer(user_details_obj).data
            logger.info("User Details Data : %s", user_details_data)
            serializer_data.update(user_details_data)
            # login_response = serializer_data
             

            login_response = {
                'access_token': serializer_data.get('access'),
                'refresh_token': serializer_data.get('refresh'),
            }
            http_status = status.HTTP_200_OK
        else:
            logger.info("Invalid User")
            login_response['message'] = "Invalid Username or Password"
            http_status = status.HTTP_401_UNAUTHORIZED
        return Response(login_response, status=http_status)

class CreateUser(APIView):
    ''' Register User '''
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        ''' Register User '''
        logger.info("User Create Request Data : %s", request.data)
        request_data = request.data
        current_user = request.user
        response = {}
        http_status = None
        try:
            serializer = SignUpSerializer(data=request_data)
            if serializer.is_valid():
                user_data = {
                    "username": request_data['username'],
                    "password": request_data['password'],
                    "first_name": request_data['first_name'],
                    "last_name": request_data['last_name'],
                    "email": request_data['email']
                }
                user_instance = User.objects.create_user(**user_data)
                logger.info("User Instance : %s", user_instance.id)
                user_details = {
                    "user": user_instance,
                    "phone": request_data['phone'],
                    "created_by": current_user.id
                }
                UserDetails.objects.create(**user_details)
                response["message"] = "User Created Successfully"
                http_status = status.HTTP_201_CREATED
            else:
                logger.info("Serializer Error : %s", serializer.errors)
                error_message = serializer_error_format(serializer.errors)
                response["errors"] = error_message
                http_status = status.HTTP_400_BAD_REQUEST

            return Response(
                response,
                status=http_status
            )
        except Exception as exp:
            logger.exception("User Create Exception : %s", exp)
            response['errors'] = "Server Error"
            http_status = status.HTTP_400_BAD_REQUEST
            return Response(
                response,
                status=http_status
            )

class VerifyUserToken(TokenVerifyView):
    ''' Verify Token '''
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        ''' Verify Token '''
        response = {}
        http_status = None
        data = request.data
        logger.info("Request Data : %s", data)
        serializer = UserTokenVerifySerializer()
        try:
            serializer_data = serializer.validate(attrs=data)
            logger.info("Serializer Data : %s ", serializer_data)
            http_status = status.HTTP_200_OK
        except Exception as exp:
            logger.exception(exp)
            response['error'] = exp.__class__.__name__
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(response, status=http_status)