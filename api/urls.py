from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.list_create_products),
    path('products/<int:id>/', views.detail_update_delete_product),
    path('product-images/', views.create_product_image),
    path('product-images/<int:id>/', views.delete_product_image),
    path('product-images/', views.delete_product_image),
    path('product-attributes/', views.create_product_attr),
    path('product-attributes/<int:id>/', views.update_delete_product_attr),
]