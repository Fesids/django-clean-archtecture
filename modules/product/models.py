from django.db import models

# Create your models here.

class Product(models.Model):
    
    userId = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length = 255, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    
    
    class Meta:
        db_table = "products"