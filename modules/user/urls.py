from django.urls import path, include
from . import views


user_urls = [
    
    path("", views.TesteViewSet.as_view({
        "get": "teste"
    })),
    
    path('create', views.UserCreateView.as_view(), name="user_create"),
    path('login', views.UserLogin.as_view(), name="login")
    
]

user_api_urlpatterns = [
    path('users/', include(user_urls))
]