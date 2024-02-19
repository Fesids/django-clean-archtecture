from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None, role=None):
        
        if not email:
            raise TypeError("A user must've a email")
        if not username:
            raise TypeError("A user must've a username")
        
        email = self.normalize_email(email)
        user.role = role
        user = self.model(username=username, email=email)
        user.set_password(password)
        
        user.save()
        return user
    
    def create_superuser(self, username=None, password=None, email=None):
        if not password:
            raise TypeError("Password should not be none")
        
        user = self.create_user(username=username, password=password,
                                email=email, role='admin')
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user
    
      


class CustomUserModel(AbstractUser, PermissionsMixin):
    
    USER_ROLE = [('admin', 'Admin'), ('client', 'Client')]
    email = models.CharField(max_length=255, unique=True, null=False, blank=False)
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    #password = models.CharField(max_length=255, null=False, blank=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, default='client', choices=USER_ROLE, null=False, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    
    objects = UserManager()
    
    def __str__(self) -> str:
        return self.email
    
    
    def to_dict(self):
        return {
			'id': self.id,
			'username': self.username,
            'email': self.email,
            'password': self.password,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'role': self.role,
			'created_at': self.created_at.isoformat(),
			'updated_at': self.updated_at.isoformat(),
			'is_active': self.is_active,
			'is_staff': self.is_staff,
		}
    
    class Meta:
        db_table = "users"