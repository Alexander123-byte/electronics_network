# network/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import NetworkNode
from .serializers import (
    NetworkNodeSerializer,
    NetworkNodeCreateUpdateSerializer
)
from .filters import NetworkNodeFilter
from .permissions import IsActiveEmployee


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления звеньями сети.
    Запрещено обновление поля 'debt' через API.
    """
    queryset = NetworkNode.objects.all().select_related(
        'contact', 'supplier'
    ).prefetch_related('products')
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NetworkNodeFilter
    search_fields = ['name', 'contact__city', 'contact__country']
    ordering_fields = ['name', 'level', 'debt', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action in ['create', 'update', 'partial_update']:
            return NetworkNodeCreateUpdateSerializer
        return NetworkNodeSerializer

    @action(detail=False, methods=['get'], url_path='factories')
    def factories(self, request):
        """Получение всех заводов (уровень 0)"""
        factories = self.get_queryset().filter(level=0)
        serializer = self.get_serializer(factories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='retailers')
    def retailers(self, request):
        """Получение всех розничных сетей (уровень 1)"""
        retailers = self.get_queryset().filter(level=1)
        serializer = self.get_serializer(retailers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='entrepreneurs')
    def entrepreneurs(self, request):
        """Получение всех ИП (уровень 2)"""
        entrepreneurs = self.get_queryset().filter(level=2)
        serializer = self.get_serializer(entrepreneurs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='debt-info')
    def debt_info(self, request, pk=None):
        """Получение информации о задолженности"""
        node = self.get_object()
        return Response({
            'node_name': node.name,
            'debt': node.debt,
            'supplier': node.supplier.name if node.supplier else None,
            'level': node.level,
            'level_display': node.get_level_display_name()
        })
