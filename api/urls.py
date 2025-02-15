from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)

urlpatterns = [
    path('product-images/', views.CreateProductImageApiView.as_view()),
    path('product-images/<int:id>/', views.DeleteProductImageApiView.as_view()),

    path('product-attributes/', views.CreateProductAttrApiView.as_view()),
    path('product-attributes/<int:id>/', views.UpdateDeleteProductAttrApiView.as_view()),

    path('categories/', views.ListCreateCategoryApiView.as_view()),
    path('categories/<int:id>/', views.UpdateDeleteProductCategory.as_view()),
    
    path('tags/', views.ListCreateProductTags.as_view()),
    path('tags/<int:id>/', views.UpdateDeleteProductTagApiView.as_view()),

    path('auth/', include('api.auth.urls')),

    path('', include(router.urls))
]