from pprint import pprint

from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ListProductSerializer, DetailProductSerializer, CreateProductSerializer
from store.models import Product


@api_view(['GET', 'POST'])
def list_products(request):

    if request.method == 'POST':
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            read_serializer = DetailProductSerializer(product, context={'request': request})
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    products = Product.objects.all()
    serializer = ListProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def detail_product(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = DetailProductSerializer(product,  context={'request': request})
    return Response(serializer.data)