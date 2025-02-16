from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import ProductFilter
from api.mixins import SuperGenericAPIView, UltraModelViewSet
from api.paginations import SimplePagination
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsSalesmanOrReadOnly, IsSalesman, IsOwner
from api.serializers import ListProductSerializer, DetailProductSerializer, CreateProductSerializer, TagSerializer, \
    UpdateProductSerializer, ProductImageSerializer, ProductAttributeSerializer, \
    UpdateProductAttributeSerializer, CategorySerializer, ProductSerializer
from store.models import Product, ProductAttribute, ProductImage, Category, Tag

class ProductViewSet(UltraModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'list': ListProductSerializer,
        'retrieve': DetailProductSerializer,
        'create': CreateProductSerializer,
        'update': UpdateProductSerializer,
    }
    pagination_class = SimplePagination
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description', 'content']
    ordering_fields = ['price', 'name', 'is_published', 'rating']
    # filterset_fields = ['category', 'tags', 'user', 'is_published']
    filterset_class = ProductFilter
    permission_classes_by_action = {
        'list':  [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated, IsSalesman],
        'update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }

    # @action(methods=['GET'], url_path='custom-action', detail=False)
    # def custom_action(self, request, *args, **kwargs):
    #     return Response({'message': 'Hello world'})




class ProductImageViewSet(UltraModelViewSet):
    
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()



class CategoryViewSet(UltraModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()





class ProductTagsViewSet(UltraModelViewSet):
    
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]



class ProductAttributesViewSet(UltraModelViewSet):
    serializer_class = ProductAttributeSerializer
    queryset = ProductAttribute.objects.all()
    
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]