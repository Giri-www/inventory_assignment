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

    # @swagger_auto_schema(tags=['Login-Authentication'], operation_description="Login url to get access token", operation_summary="Login",
    #                      request_body=LoginSerializer, responses=login_response_schema_dict)
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
            # access_token =   
            # refresh_token =   

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

    # @swagger_auto_schema(tags=['User'], operation_description="Create User", operation_summary="User Create", request_body=SignUpSerializer)
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


class UpdateUser(APIView):
    ''' Update User '''
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        query = User.objects.filter(
            id=user_id)
        return query

    def get_object(self):
        queryset = self.get_queryset()
        qfilter = {}
        obj = get_object_or_404(queryset, **qfilter)
        return obj

    def get_serializer_class(self):
        return UserDetailsSerializer

    # @swagger_auto_schema(tags=['User'], operation_description="Update User", operation_summary="User Update", request_body=UserUpdateSerializer)
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        ''' Update User '''
        logger.info("User Update Request Data : %s", request.data)
        request_data = request.data
        response = {}
        http_status = None
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        current_user = request.user

        try:
            serializer = UserUpdateSerializer(data=request_data)
            if serializer.is_valid():
                user_data = {
                    "first_name": request_data['first_name'],
                    "last_name": request_data['last_name'],
                    "email": request_data['email']
                }
                user_instance = self.get_queryset()
                user_instance.update(**user_data)
                user_details = {
                    "phone": request_data['phone'],
                    "updated_by": current_user.id
                }
                UserDetails.objects.filter(
                    user_id=user_id).update(**user_details)
                response["message"] = "User Updated Successfully"
                http_status = status.HTTP_200_OK
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


# def filter_query(request_data, filterquery):
#     '''Retrieve employee filter data'''
#     for i in request_data:
#         filter_val = request_data[i][0]
#         if i == 'user_full_name':
#             i = i.replace('user_full_name', 'user_id')
#             filterquery.add(Q(**{i+"__in": User.objects.annotate(full_name=Concat(
#                 'first_name', Value(' '), 'last_name', output_field=CharField())).filter(full_name__iexact=filter_val).values_list('id', flat=True)}), Q.AND)
#         else:
#             filterquery.add(
#                 Q(**{str(i): filter_val}), Q.AND)
#     return filterquery


# user_params = [
#     openapi.Parameter("user_full_name",
#                       openapi.IN_QUERY,
#                       description="User Full Name",
#                       type=openapi.TYPE_STRING
#                       )
# ]


# class UserListViews(ListModelMixin, GenericAPIView):
#     ''' User List Views Class '''
#     queryset = UserDetails.objects.all()
#     # pagination_class = None
#     permission_classes = [AllowAny]
#     serializer_class = UserDetailsSerializer
#     filter_backends = [DjangoFilterBackend,
#                        filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['user_id', 'user_type',
#                         'phone', 'organization_id', 'user__email']
#     ordering_fields = '__all__'
#     ordering = ['-user_details_id']

#     @swagger_auto_schema(tags=['User'],
#                          operation_description="User List",
#                          operation_summary="User List", manual_parameters=user_params)
#     def get(self, request, *args, **kwargs):
#         ''' User List Get '''
#         resp = {}
#         try:
#             logger.info("User Get Request Data : %s", request.GET)
#             user_id = request.GET.get('user_id')
#             logger.info("User ID : %s", user_id)
#             user_count = self.queryset.count()
#             page = request.GET.get('page', 1)
#             page_size = request.GET.get('page_size', 50)
#             logger.info("User ID : %s", user_id)
#             limit = int(page_size)
#             page = int(page)
#             offset = (page - 1) * limit
#             current_user = request.user
#             logger.info("Current User : %s", current_user.id)
#             page_count = user_count / int(page_size) if page_size else 0
#             copy_request_data = deepcopy(dict(request.GET))
#             filterquery = Q()
#             if user_id is None:
#                 copy_request_data.pop('ordering', None)
#                 copy_request_data.pop('page', None)
#                 copy_request_data.pop('page_size', None)
#                 copy_request_data.pop('search', None)
#                 filterquery = filter_query(copy_request_data, filterquery)
#                 logger.info("Filter Query : %s", filterquery)
#                 current_user_obj = UserDetails.objects.get(
#                     user_id=current_user.id)
#                 current_user_control = current_user_obj.user_type.user_control
#                 logger.info("Current User Control : %s", current_user_control)
#                 user_type_list = list(
#                     map(lambda x: x['user_type_id'], current_user_control['can_create']))
#                 logger.info("User Type List : %s", user_type_list)
#                 user_list_obj = UserDetails.objects.filter(
#                     Q(user_type_id__in=user_type_list) & Q(filterquery)).order_by('-user_details_id')
#                 total = user_list_obj.count()
#                 paginated_data = user_list_obj[offset:offset+limit]
#                 response_data = UserDetailsSerializer(
#                     paginated_data, many=True).data
#                 page_count = total / int(page_size) if page_size else 0
#                 list_response = {
#                     "total": total,
#                     "page": page,
#                     "page_size": limit,
#                     "page_count": math.ceil(page_count),
#                     "results": response_data
#                 }

#                 return Response(list_response)
#             else:
#                 queryset = UserDetails.objects.filter(user_id=user_id)
#                 if not queryset.exists():
#                     resp['errors'] = "Invalid User ID"
#                     return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                 response_data = UserDetailsSerializer(queryset.first())
#                 return Response(response_data.data)
#         except Exception as exp:
#             logger.exception("User List Get Exception : %s", exp)
#             resp['errors'] = "Server Error"
#             return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyUserToken(TokenVerifyView):
    ''' Verify Token '''
    permission_classes = (AllowAny,)

    # @swagger_auto_schema(tags=['Login-Authentication'], operation_description="Verify User Token", operation_summary="Verify User Token", request_body=UserTokenVerifySerializer)
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