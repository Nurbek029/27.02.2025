import django_filters
from .models import Product

class ProductListFilter(django_filters.FilterSet):
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('category', 'price')  # Только реальные поля модели
