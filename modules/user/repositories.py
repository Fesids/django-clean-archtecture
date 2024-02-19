from core.utils.exception_utils import AppExceptionHelper, AppRepositoryException
from .models import CustomUserModel as User
from django.contrib import auth
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

class UserRepository(AppExceptionHelper):
    def user_repo_get_by_email(self, email, password):
        try:
            return get_object_or_404(User, email=email)
            #return auth.authenticate(email=email, password=password)
        except User.password != password:
             raise AppRepositoryException(
                field="User",
                message="Failed trying to retrive user",
                error_info=f"Password not valid",
                child_error=exception
            )
        except User.DoesNotExist as exception:
            self.raise_repository_instance_not_found_exception(field="User", exception_type="UserNotFound")
        except Exception as exception:
            raise AppRepositoryException(
                field="User",
                message="Failed trying to retrieve user",
                error_info=f"Retrieve User where resource: {email} was process failed",
                child_error=exception
            )
    
    @transaction.atomic
    def user_repo_create(self, user):
        with transaction.atomic():
            try:
                return User.objects.create(**user)
            except Exception as exception:
                raise AppRepositoryException(
                    field="User",
                    message="Create User was process failed",
                    error_info=f"Create user was process failed",
                    child_error=exception
                )