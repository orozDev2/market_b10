from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveDestroyAPIView, UpdateAPIView, RetrieveUpdateAPIView,
                                    RetrieveUpdateDestroyAPIView)
from django.core.paginator import Paginator

from api.filters import ProductFilter
from api.serializers import ListProductSerializer, DetailProductSerializer, CreateProductSerializer, \
    UpdateProductSerializer, ProductImageSerializer, ProductAttributeSerializer, \
    UpdateProductAttributeSerializer
from store.models import Product, ProductImage, ProductAttribute


class ProductListAPIView(ListAPIView):
    serializer_class = ListProductSerializer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'content', 'tags__name']




class ProductCreateAPIView(CreateAPIView):
    serializer_class = CreateProductSerializer
    queryset = Product.objects.all()  


class ProductDetailAPIView(RetrieveDestroyAPIView):
    serializer_class = DetailProductSerializer
    queryset = Product.objects.all() 
    lookup_field = 'id' 


class ProductUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UpdateProductSerializer
    queryset = Product.objects.all() 
    lookup_field = 'id' 


# @api_view(['GET', 'POST'])
# def list_create_products(request):
#     if request.method == 'POST':
#         serializer = CreateProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         product = serializer.save()
#         read_serializer = DetailProductSerializer(product, context={'request': request})
#         return Response(read_serializer.data, status=status.HTTP_201_CREATED)

#     products = Product.objects.all()

#     # SEARCH
#     search = request.GET.get('search')
#     if search:
#         products = products.filter(
#             Q(name__icontains=search) |
#             Q(description__icontains=search) |
#             Q(content__icontains=search) |
#             Q(tags__name__icontains=search)
#         ).distinct()

#     # FILTERING
#     filterset = ProductFilter(queryset=products, data=request.GET)
#     products = filterset.qs

#     # ORDERING
#     ordering_fields = ['name', 'price', 'rating', 'created_at']
#     ordering: str = request.GET.get('ordering', '')
#     tem_ordering = ordering.split('-')[1] if ordering.startswith('-') else ordering

#     if tem_ordering in ordering_fields:
#         products = products.order_by(ordering)

#     # PAGINATION
#     product_count = products.count()

#     page = int(request.GET.get('page', 1))
#     page_size = int(request.GET.get('page_size', 12))
#     pagin = Paginator(products, page_size)
#     products = pagin.get_page(page)

#     serializer = ListProductSerializer(products, many=True, context={'request': request})

#     return Response({
#         'page': page,
#         'page_size': page_size,
#         'count': product_count,
#         'results': serializer.data
#     })


@api_view(['GET', 'PATCH', 'PUT', "DELETE"])
def detail_update_delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method in ['PATCH', 'PUT']:
        partial = request.method == 'PATCH'
        serializer = UpdateProductSerializer(instance=product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = DetailProductSerializer(product, context={'request': request})
        return Response(read_serializer.data)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = DetailProductSerializer(product, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
def create_product_image(request):
    serializer = ProductImageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_product_image(request, id):
    product_image = get_object_or_404(ProductImage, id=id)
    product_image.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_product_attr(request):
    serializer = ProductAttributeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['PUT', 'PATCH', 'DELETE'])
def update_delete_product_attr(request, id):
    product_attr = get_object_or_404(ProductAttribute, id=id)

    if request.method in ['PATCH', 'PUT']:
        partial = request.method == 'PATCH'
        serializer = UpdateProductAttributeSerializer(instance=product_attr, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        product_attr.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
