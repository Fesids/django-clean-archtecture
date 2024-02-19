from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import filters, views, viewsets, status, permissions, decorators as rest_decorators, request, authentication
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt import views, tokens, serializers as jwt_serializer, exceptions as jwt_exceptions
from django.conf import settings
#import core.settings as settings
from django.middleware import csrf
from django.contrib import auth

### 
from core.utils.base_view_utils import APIResponseView, CustomPagination, PaginationAPIResponse
from core.utils.exception_utils import AppRequestException
from modules.user.repositories import UserRepository
from modules.user.serializers import UserSerializer, UserGetSerializer
from modules.user.filters import UserFilter

# Create your views here.


def generate_user_token(user):
    refresh = tokens.RefreshToken.for_user(user)
    
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }


class TesteViewSet(viewsets.ViewSet):
    
    def teste(self, request, *args, **kwargs):
        return Response("teste", status=status.HTTP_200_OK)
    
    
    
class UserCreateView(APIResponseView):
    serializer_class = UserSerializer
    
    repo = UserRepository()
    queryset = None
    
    def perform_create_logic(self, payload):
        try:
            serializer = self.serializer_class(data=payload)
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                instance = self.repo.user_repo_create(validated_data)
                re_serialize = self.serializer_class(instance)
                response = re_serialize.data
                return response 
        except Exception as exception:
            raise AppRequestException(
                field="User",
                message="The process create user was filed",
                error_info="The  process perform logic to create was failed",
                child_error=exception
            )
            
    def post(self, request):
        try:
            request_data = request.data
            response = self.perform_create_logic(request_data)
            
            return self.handle_created_response(
                description=f"User created successfully",
                message_code="Created",
                status_code=status.HTTP_201_CREATED,
                response=response
            )
            
        except Exception as exception:
            return self.handle_error_response(
                exception=exception,
                status_code=status.HTTP_400_BAD_REQUEST,
                message_code="Bad Request",
                description=f"Failed to create new user"
            )
        
class UserLogin(APIResponseView):
    serializer_class = UserGetSerializer
    repo = UserRepository()
    queryset = None  
    
    def perform_get_logic(self, email, password):
        try:
            self.queryset = self.repo.user_repo_get_by_email(email=email, password=password)
            if self.queryset:
                serializer = self.serializer_class(self.queryset, many=False)
                return serializer.data
        except Exception as exception:
            raise AppRequestException(
                field="User",
                message="The process get user was filed",
                error_info="The process perform logic to get user was failed",
                child_error=exception
            )
    
    def perform_generate_token(self, user):
        #user = auth.authenticate(email=email, password=password)
        token = ""#generate_user_token(user)
        response = Response()
        print(user)
        if user is not None:
            token = generate_user_token(user)
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=tokens["access_token"],
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]

            )

            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                value=tokens["refresh_token"],
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]

            )
            
            response.data = token
        
            response["X-CSRFToken"] = csrf.get_token(request)
            
            return response
        else:
            return "prr"
        
    def post(self, request):
        password = request.data["password"]
        email = request.data["email"]
        try:
            response_user = self.perform_get_logic(email=email, password=password)
            response_token = ""#self.perform_generate_token(user={id: response_user.id})
            
            #print(response_token)
            #print(response_user)
            if response_user:
                return self.handle_success_response(
                    description=f"User retrive successfully",
                    message_code="Success",
                    status_code=status.HTTP_200_OK,
                    response=response_user
                )
            else:
                return self.handle_error_response(
                    exception=None,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message_code="Bad Request",
                    description=f"Get User failed"
                )
        except Exception as exception:
            return self.handle_error_response(
                exception=exception,
                status_code=status.HTTP_400_BAD_REQUEST,
                message_code="Bad Request",
                description=f"Get User failed"
            )