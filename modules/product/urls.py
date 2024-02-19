from . import views
from django.urls import path, include

product_urls = [
    path('/teste', views.Teste.as_view(), name="teste"),
    path("/create", views.ProductCreateView.as_view(), name="create"),
    path("/<int:id>", views.ProductGetView.as_view(), name="get"),
     path("/delete/<int:id>", views.ProductDeleteView.as_view(), name="delete")
]

product_api_urlpatterns = [
    path('products', include(product_urls))
]