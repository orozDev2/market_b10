from django.db.models import Q
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
# from rest_framework.decorators import authentication_classes, permission_classes
from django.core.paginator import Paginator
from rest_framework.views import APIView

from api.filters import ProductFilter
from api.permissions import IsAdminOrReadOnly
from api.serializers import ListProductSerializer, DetailProductSerializer, CreateProductSerializer, TagSerializer, \
    UpdateProductSerializer, ProductImageSerializer, ProductAttributeSerializer, \
    UpdateProductAttributeSerializer, CategorySerializer
from store.models import Product, ProductAttribute, ProductImage, Category, Tag
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def list_create_products_api_view(request):...


class ListCreateProductApiView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

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


class CreateProductAttrApiView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ProductAttributeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class UpdateDeleteProductAttrApiView(APIView):
    
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
        product_attr.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateProductImageApiView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class DeleteProductImageApiView(APIView):
    
    def delete(self, request, id, *args, **kwargs):
        product_image = get_object_or_404(ProductImage, id=id)
        product_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateCategoryApiView(APIView):

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class UpdateDeleteProductCategory(APIView):
    
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def update(self, request, id, partial, *args, **kwargs):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def get(self, request, id, *args, **kwargs):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, id, *args, **kwargs):
        return self.update(request, id, partial=False)
    
    def patch(self, request, id, *args, **kwargs):
        return self.update(request, id, partial=True)
    
    def delete(self, request, id, *args, **kwargs):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class ListCreateProductTags(APIView):
    
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    
    
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    
class UpdateDeleteProductTagApiView(APIView):
    
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    
    def update(self, request, id, partial, *args, **kwargs):
        tag = get_object_or_404(Tag, id=id)
        serializer = TagSerializer(tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def get(self, request, id,*args, **kwargs):
        tag = get_object_or_404(Tag, id=id)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    def put(self, request, id, *args, **kwargs):
        return self.update(request, id, partial=False)
    
    def patch(self, request, id, *args, **kwargs):
        return self.update(request, id, partial=True)
    
    def delete(self, request, id, *args, **kwargs):
        tag = get_object_or_404(Tag, id=id)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)