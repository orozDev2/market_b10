from django_filters import rest_framework as filterset

from store.models import Product, Category


class ProductFilter(filterset.FilterSet):

    categories = filterset.ModelMultipleChoiceFilter(queryset=Category.objects.all(), field_name='category')
    min_price = filterset.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filterset.NumberFilter(field_name='price', lookup_expr='lte')
    receive_types = filterset.MultipleChoiceFilter(choices=Product.RECEIVE_TYPE, field_name='receive_type')

    class Meta:
        model = Product
        fields = [
            'tags',
            'user',
            'is_published',
            'rating',
        ]