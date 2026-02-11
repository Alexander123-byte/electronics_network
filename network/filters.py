import django_filters
from .models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    """Фильтр для модели NetworkNode"""
    country = django_filters.CharFilter(
        field_name='contact__country',
        lookup_expr='icontains',
        label='Страна'
    )
    city = django_filters.CharFilter(
        field_name='contact__city',
        lookup_expr='icontains',
        label='Город'
    )
    level = django_filters.NumberFilter(
        field_name='level',
        label='Уровень иерархии'
    )
    created_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Создано после'
    )
    created_before = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Создано до'
    )

    class Meta:
        model = NetworkNode
        fields = ['country', 'city', 'level']
