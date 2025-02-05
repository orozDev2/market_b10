from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.ListCreateProductApiView.as_view()),
    path('products/<int:id>/', views.UpdateDeleteDetailProductApiView.as_view()),
    path('product-images/', views.create_product_image),
    path('product-images/<int:id>/', views.delete_product_image),
    path('product-images/', views.delete_product_image),
    path('product-attributes/', views.create_product_attr),
    path('product-attributes/<int:id>/', views.update_delete_product_attr),

    path('auth/', include('api.auth.urls')),
]