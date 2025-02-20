from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as url_doc
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('tags', views.ProductTagsViewSet)

urlpatterns = [
    path('product-images/', views.CreateProductImageApiView.as_view()),
    path('product-images/<int:id>/', views.DeleteProductImageApiView.as_view()),

    path('product-attributes/', views.CreateProductAttrApiView.as_view()),
    path('product-attributes/<int:id>/', views.UpdateDeleteProductAttrApiView.as_view()),
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls))
]

urlpatterns += url_doc