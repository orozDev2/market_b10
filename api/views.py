from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
# from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import APIView

from api.filters import ProductFilter
from api.mixins import SerializerByMethodMixin, ResponseSerializerMixin, SuperGenericAPIView
from api.paginations import SimplePagination
from api.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from api.serializers import ListProductSerializer, DetailProductSerializer, CreateProductSerializer, TagSerializer, \
    UpdateProductSerializer, ProductImageSerializer, ProductAttributeSerializer, \
    UpdateProductAttributeSerializer, CategorySerializer
from store.models import Product, ProductAttribute, ProductImage, Category, Tag


# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def list_create_products_api_view(request):...


class ListCreateProductApiView(SuperGenericAPIView):
    queryset = Product.objects.all()
    serializer_classes = {
        'GET': ListProductSerializer,
        'POST': CreateProductSerializer,
    }
    response_serializer = DetailProductSerializer
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        products = self.filter_queryset(self.get_queryset())
        products = self.paginate_queryset(products)
        serializer = self.get_serializer(products, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = self.get_response_serializer(product)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class UpdateDeleteDetailProductApiView(SuperGenericAPIView):
    queryset = Product.objects.all()
    serializer_class = DetailProductSerializer
    serializer_classes = {
        'GET': DetailProductSerializer,
        'PATCH': UpdateProductSerializer,
        'PUT': UpdateProductSerializer,
    }
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def update(self, request, partial):
        product = self.get_object()
        serializer = self.get_serializer(instance=product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = self.get_serializer(product)
        return Response(read_serializer.data)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.update(request, True)

    def put(self, request, *args, **kwargs):
        return self.update(request, False)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateProductAttrApiView(SuperGenericAPIView):
    
    serializer_class = ProductAttributeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class UpdateDeleteProductAttrApiView(SuperGenericAPIView):
    
    queryset = ProductAttribute.objects.all()
    serializer_classes = {
        'GET': ProductAttributeSerializer,
        'PATCH': UpdateProductAttributeSerializer,
        'PUT': UpdateProductAttributeSerializer,
    }
    lookup_field = 'id'

    def update(self, request, partial):
        product_attr = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(product_attr, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, id, *args, **kwargs):
        product_attr = get_object_or_404(ProductAttribute, id=id)
        serializer = ProductAttributeSerializer(product_attr)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=False)

    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True)

    def delete(self, request, id, *args, **kwargs):
        product_attr = get_object_or_404(ProductAttribute, id=id)
        product_attr.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateProductImageApiView(SuperGenericAPIView):
    
    serializer_class = ProductImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteProductImageApiView(SuperGenericAPIView):
    
    queryset = ProductImage.objects.all()

    def delete(self, request, *args, **kwargs):
        product_image = self.get_object()
        product_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateCategoryApiView(SuperGenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class UpdateDeleteProductCategory(SuperGenericAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'

    def update(self, request, partial, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=False)

    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True)

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateProductTags(SuperGenericAPIView):
    
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    # def get(self, request, *args, **kwargs):
    #     tags = self.get_object()
    #     serializer = self.get_serializer(tags, many=True)
    #     return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateDeleteProductTagApiView(SuperGenericAPIView):
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'

    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def update(self, request, partial, *args, **kwargs):
        tag = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        tag = self.get_object()
        serializer = self.get_serializer(tag)
        return Response(serializer.data)

    def put(self, request,  *args, **kwargs):
        return self.update(request, partial=False)

    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True)

    def delete(self, request, id, *args, **kwargs):
        tag = get_object_or_404(Tag, id=id)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
