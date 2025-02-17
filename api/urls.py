from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('images', views.ProductImageViewSet)
router.register('categories', views.CategoryViewSet)
router.register('tags', views.ProductTagsViewSet)
router.register('attributes', views.ProductAttributesViewSet)

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls))
]