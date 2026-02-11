from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import NetworkNode
from .serializers import (
    NetworkNodeSerializer,
    NetworkNodeCreateUpdateSerializer
)
from .filters import NetworkNodeFilter


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления звеньями сети.
    Запрещено обновление поля 'debt' через API.
    """
    queryset = NetworkNode.objects.all().select_related(
        'contact', 'supplier'
    ).prefetch_related('products')
    permission_classes = [IsAuthenticated]
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

    @action(detail=False, methods=['get'])
    def factories(self, request):
        """Получение всех заводов (уровень 0)"""
        factories = self.queryset.filter(level=0)
        serializer = self.get_serializer(factories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def retails(self, request):
        """Получение всех розничных сетей (уровень 1)"""
        retails = self.queryset.filter(level=1)
        serializer = self.get_serializer(retails, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def entrepreneurs(self, request):
        """Получение всех ИП (уровень 2)"""
        entrepreneurs = self.queryset.filter(level=2)
        serializer = self.get_serializer(entrepreneurs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def debt_info(self, request, pk=None):
        """Получение информации о задолженности"""
        node = self.get_object()
        return Response({
            'node_name': node.name,
            'debt': node.debt,
            'supplier': node.supplier.name if node.supplier else None
        })
