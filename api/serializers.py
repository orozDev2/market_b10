from rest_framework import serializers

from store.models import Product, ProductAttribute, Category, Tag, ProductImage


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        exclude = ('product',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class ListProductSerializer(serializers.ModelSerializer):

    # image1 = serializers.ImageField(source='image')
    # category = serializers.CharField(source='category.name')
    # tags = serializers.ListSerializer(child=serializers.CharField(source='tags.name'))
    image = serializers.ImageField()
    attributes = ProductAttributeSerializer(many=True)
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('content',)


class DetailProductSerializer(serializers.ModelSerializer):

    # image1 = serializers.ImageField(source='image')
    # category = serializers.CharField(source='category.name')
    # tags = serializers.ListSerializer(child=serializers.CharField(source='tags.name'))
    image = serializers.ImageField()
    attributes = ProductAttributeSerializer(many=True)
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
