from pprint import pprint

from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ListProductSerializer, DetailProductSerializer, CreateProductSerializer, \
    UpdateProductSerializer, ProductImageSerializer, ProductAttributeSerializer, \
    UpdateProductAttributeSerializer
from store.models import Product, ProductImage, ProductAttribute


@api_view(['GET', 'POST'])
def list_create_products(request):

    if request.method == 'POST':
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = DetailProductSerializer(product, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    products = Product.objects.all()
    serializer = ListProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


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

    serializer = DetailProductSerializer(product,  context={'request': request})
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