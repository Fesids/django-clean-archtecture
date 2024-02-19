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
from modules.product.repositories import ProductRepository
from modules.product.serializers import ProductSerializer, ProductDeleteSerializer
from modules.user.filters import UserFilter
import json


# Create your views here.


class Teste(APIResponseView):
    
    def get(self, request):
        
        return self.handle_success_response(
            description="teste",
            message_code="Ok",
            status_code=status.HTTP_200_OK,
            response="teste"
            
        )
        
class ProductDeleteView(APIResponseView):
    serializer_class = ProductDeleteSerializer#ProductSerializer
    repo = ProductRepository()
    queryset = None
    
    def perform_delete_logic(self, id):
       
        try:
            self.queryset = self.repo.product_repo_delete_by_id(id)
            if self.queryset:
                serializer = self.serializer_class(self.queryset, many=False)
                return serializer.data
            
        except Exception as exception:
            raise AppRequestException(
                field="product",
                message="The proccess get product was filed",
                error_info="The proccess perform logic to get product was failed",
                child_error=exception
            )

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get("id")
        try:
            response_product = self.perform_delete_logic(product_id)
            
            return self.handle_success_response(
                description=f"Product deleted successfully",
                message_code="Success",
                status_code=status.HTTP_200_OK,
                response=response_product
            )
           
                
        except Exception as exception:
                raise self.handle_error_response(
                    exception=exception,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message_code="Bad request",
                    description=f"Delete product failed"
                )
                 
class ProductGetView(APIResponseView):
    serializer_class = ProductSerializer
    repo = ProductRepository()
    queryset = None
    
    def perform_get_logic(self, **kwargs):
        product_id = kwargs.get("id")
        print(kwargs)
        try:
            self.queryset = self.repo.product_repo_get_by_id(product_id)
            if self.queryset:
                serializer = self.serializer_class(self.queryset, many=False)
                return serializer.data
        except Exception as exception:
            raise AppRequestException(
                field="product",
                message="The proccess get product was filed",
                error_info="The proccess perform logic to get product was failed",
                child_error=exception
            )
            
    
    def get(self, request, *args, **kwargs):
        try:
            response_product = self.perform_get_logic(**kwargs)
            
            if response_product:
                return self.handle_success_response(
                    description=f"Product retrive successfully",
                    message_code="Success",
                    status_code=status.HTTP_200_OK,
                    response=response_product
                )
            else:
                return self.handle_error_response(
                    exception=None,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message_code="Bad Request",
                    description=f"Get product failed"
                )
                
        except Exception as exception:
                raise self.handle_error_response(
                    exception=exception,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message_code="Bad request",
                    description=f"Get product failed"
                )
            
class ProductCreateView(APIResponseView):
    serializer_class = ProductSerializer
    repo = ProductRepository()
    queryset = None
    
    def perform_create_logic(self, payload):
        
        try:
            serializer = self.serializer_class(data=payload)
            
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                instance = self.repo.prouct_repo_create(validated_data)
                re_serialize= self.serializer_class(instance)
                response = re_serialize.data
                return response
        except Exception as exception:
            raise AppRequestException(
                field="product",
                message="The process create product was filed",
                error_info="The  process perform logic to create product was failed",
                child_error=exception
            )
    
    def post(self, request):
        try:
            request_data = request.data
            response = self.perform_create_logic(request_data)
            
            return self.handle_created_response(
                description=f'Product created successfully',
                message_code='Created',
                status_code=status.HTTP_201_CREATED,
                response=response
            )
            
        except Exception as exception:
            return self.handle_error_response(
                exception=exception,
                status_code=status.HTTP_400_BAD_REQUEST,
                message_code="Bad Request",
                description=f"failed to create a new product"
            )