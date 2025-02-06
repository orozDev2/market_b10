from django.urls import path, include
from . import views

urlpatterns =[
    path('products/', views.ListCreateProductApiView.as_view()),
    path('products/<int:id>/', views.UpdateDeleteDetailProductApiView.as_view()),

    path('product-images/', views.CreateProductImageApiView.as_view()),
    path('product-images/<int:id>/', views.DeleteProductImageApiView.as_view()),

    path('product-attributes/', views.CreateProductAttrApiView.as_view()),
    path('product-attributes/<int:id>/', views.UpdateDeleteProductAttrApiView.as_view()),

    path('categories/', views.ListCreateCategoryApiView.as_view()),
    path('categories/<int:id>/', views.UpdateDeleteProductCategory.as_view()),
    
    path('tags/', views.ListCreateProductTags.as_view()),

    path('auth/', include('api.auth.urls')),
]