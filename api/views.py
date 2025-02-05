from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveDestroyAPIView, UpdateAPIView, RetrieveUpdateAPIView,
                                    RetrieveUpdateDestroyAPIView)
from django.core.paginator import Paginator
from rest_framework.views import APIView

from api.filters import ProductFilter
from api.serializers import ListProductSerializer, DetailProductSerializer, CreateProductSerializer, \
    UpdateProductSerializer, ProductImageSerializer, ProductAttributeSerializer, \
    UpdateProductAttributeSerializer
from store.models import Product, ProductImage, ProductAttribute


class ListCreateProductApiView(APIView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        # SEARCH
        search = request.GET.get('search')
        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(content__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()

        # FILTERING
        filterset = ProductFilter(queryset=products, data=request.GET)
        products = filterset.qs

        # ORDERING
        ordering_fields = ['name', 'price', 'rating', 'created_at']
        ordering: str = request.GET.get('ordering', '')
        tem_ordering = ordering.split('-')[1] if ordering.startswith('-') else ordering

        if tem_ordering in ordering_fields:
            products = products.order_by(ordering)

        # PAGINATION
        product_count = products.count()

        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 12))
        pagin = Paginator(products, page_size)
        products = pagin.get_page(page)

        serializer = ListProductSerializer(products, many=True, context={'request': request})

        return Response({
            'page': page,
            'page_size': page_size,
            'count': product_count,
            'results': serializer.data
        })

    def post(self, request, *args, **kwargs):
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = DetailProductSerializer(product, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class UpdateDeleteDetailProductApiView(APIView):

    def update(self, request, id, partial):
        product = get_object_or_404(Product, id=id)
        serializer = UpdateProductSerializer(instance=product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = DetailProductSerializer(product, context={'request': request})
        return Response(read_serializer.data)

    def get(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        serializer = DetailProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, id, *args, **kwargs):
        return self.update(request, id, True)

    def put(self, request, id, *args, **kwargs):
        return self.update(request, id, False)

    def delete(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateAttrApiView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ProductAttributeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)




class UpdateDeleteAttrApiView(APIView):
    
    def update(self, request, id, partial):
        product_attr = get_object_or_404(ProductAttribute, id=id)
        serializer = UpdateProductAttributeSerializer(data=request.data, instance=product_attr, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request, id, *args, **kwargs):
        product_attr = get_object_or_404(ProductAttribute, id=id)
        serializer = ProductAttributeSerializer(product_attr)
        return Response(serializer.data)
    
    def put(self, request, id, *args, **kwargs):
        return self.update(request, id, partial=False)
        
    def patch(self, request, id, *args, **kwargs):
        return self.update(request, id, partial=True)

    def delete(self, request, id, *args, **kwargs):
        product_attr = get_object_or_404(ProductAttribute, id=id)
        serializer = FilmAttributeSerializer(product_attr)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateImageApiView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class DeleteImageApiView(APIView):
    
    def delete(self, request, id, *args, **kwargs):
        product_image = get_object_or_404(FilmImage, id=id)
        serializer = ProductImageSerializer(product_image)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
