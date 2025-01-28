import django_filters

from store.models import Product, Category


class ProductFilter(django_filters.FilterSet):

    categories = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), field_name='category')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    receive_types = django_filters.MultipleChoiceFilter(choices=Product.RECEIVE_TYPE, field_name='receive_type')

    class Meta:
        model = Product
        fields = [
            'tags',
            'user',
            'is_published',
            'rating',
        ]