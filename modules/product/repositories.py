from core.utils.exception_utils import AppExceptionHelper, AppRepositoryException
from .models import Product
from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404


class ProductRepository(AppExceptionHelper):
  
  def product_repo_delete_by_id(self, id):
    
    try:
      product = get_object_or_404(Product, id=id)
      product.delete()
      return {}
   
    except Product.DoesNotExist as exception:
      self.raise_repository_instance_not_found_exceptio(field="Product", exception_type="ProductNotFound")
      
    except Exception as exception:
          raise AppRepositoryException(
              field="User",
              message="Failed trying to delete product",
              error_info=f"Delete product where resource: {id} was process failed",
              child_error=exception
          )
      
  
  def product_repo_get_by_id(self, id):
    try:
      return get_object_or_404(Product, id=id)
    except not id:
      raise AppRepositoryException(
        field="ID",
        message="Failed trying to retrieve product",
        error_info=f"ID not provided",
        child_error=exception
      )
    except Product.DoesNotExist as exception:
      self.raise_repository_instance_not_found_exceptio(field="Product", exception_type="ProductNotFound")
      
    except Exception as exception:
          raise AppRepositoryException(
              field="User",
              message="Failed trying to retrieve product",
              error_info=f"Retrieve product where resource: {id} was process failed",
              child_error=exception
          )
          
  @transaction.atomic
  def prouct_repo_create(self, product):
    with transaction.atomic():
      try:
        return Product.objects.create(**product)
      
      except Exception as exception:
        raise AppRepositoryException(
          field="Product",
          message="Create product failed",
          error_info=f'Create ´product process failed',
          child_error=exception
        )