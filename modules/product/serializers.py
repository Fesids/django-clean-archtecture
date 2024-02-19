from rest_framework import serializers
from core.utils.exception_utils import AppExceptionHelper, AppValidateException
from modules.product.models import Product

class ProductDeleteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
  
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
      model = Product
      fields = "__all__"
      
    def validate(self, attrs):
      return super().validate(attrs)
  
  