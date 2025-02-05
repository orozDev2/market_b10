from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ListCreateProductApiView.as_view()),
    path('products/<int:id>/', views.UpdateDeleteDetailProductApiView.as_view()),
    path('product-images/', views.CreateImageApiView.as_view()),
    path('product-images/<int:id>/', views.DeleteImageApiView.as_view()),
    path('product-attributes/', views.CreateAttrApiView.as_view()),
    path('product-attributes/<int:id>/', views.UpdateDeleteAttrApiView.as_view()),
]
