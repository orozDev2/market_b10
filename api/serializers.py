import uuid

from rest_framework import serializers

from store.models import Product, ProductAttribute, Category, Tag, ProductImage
from utils.main import base64_to_image_file


class AttributeForProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class ImageForProductSerializer(serializers.ModelSerializer):

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
    attributes = AttributeForProductSerializer(many=True)
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    images = ImageForProductSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('content',)


class DetailProductSerializer(serializers.ModelSerializer):

    # image1 = serializers.ImageField(source='image')
    # category = serializers.CharField(source='category.name')
    # tags = serializers.ListSerializer(child=serializers.CharField(source='tags.name'))
    image = serializers.ImageField()
    attributes = AttributeForProductSerializer(many=True)
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    images = ImageForProductSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):

    attributes = AttributeForProductSerializer(many=True, required=False)
    images = serializers.ListSerializer(child=serializers.CharField(), required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        attributes = validated_data.pop('attributes', [])
        images = validated_data.pop('images', [])
        tags = validated_data.pop('tags', [])

        file_images = []

        for image in images:
            try:
                file = base64_to_image_file(image, uuid.uuid4())
                file_images.append(file)
            except Exception as e:
                print(e)
                raise serializers.ValidationError(
                    {'images': ['Загрузите корректное изображение']}
                )

        product = Product.objects.create(**validated_data)
        product.tags.add(*tags)

        for attribute in attributes:
            ProductAttribute.objects.create(
                **attribute,
                product=product
            )

        for file_image in file_images:
            product_image = ProductImage.objects.create(product=product)
            product_image.image.save(file_image.name, file_image)
            product_image.save()

        return product


class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ('user',)


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = '__all__'


class UpdateProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = ('name', 'value')

