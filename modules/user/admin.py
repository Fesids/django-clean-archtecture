from django.contrib import admin
from django.apps import apps
all_models = apps.get_app_config('user').get_models()

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'email', 
        'username', 
        'password', 
        'first_name', 
        'last_name', 
        'is_active', 
        'role',
        'created_at','updated_at')
    
for model in all_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered as e:
        pass