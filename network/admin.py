from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import QuerySet
from django.http import HttpRequest
from .models import NetworkNode, Contact, Product


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'city', 'street', 'house_number')
    list_filter = ('country', 'city')
    search_fields = ('email', 'country', 'city')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')
    list_filter = ('name',)
    search_fields = ('name', 'model')


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_level_display', 'supplier_link', 'debt', 'created_at', 'city')
    list_filter = ('contact__city', 'level', 'created_at')
    search_fields = ('name', 'contact__city', 'contact__country')
    readonly_fields = ('created_at', 'level')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'level', 'created_at')
        }),
        ('Контакты', {
            'fields': ('contact',)
        }),
        ('Продукты', {
            'fields': ('products',)
        }),
        ('Поставщик и задолженность', {
            'fields': ('supplier', 'debt')
        }),
    )

    actions = ['clear_debt']

    def get_queryset(self, request):
        """Оптимизация запросов к БД"""
        return super().get_queryset(request).select_related(
            'contact', 'supplier__contact'
        ).prefetch_related('products')

    def supplier_link(self, obj):
        """Создание ссылки на поставщика в админке"""
        if obj.supplier:
            url = reverse('admin:network_networknode_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "Нет поставщика"
    supplier_link.short_description = 'Поставщик'

    def city(self, obj):
        """Получение города из связанных контактов"""
        return obj.contact.city if obj.contact else "-"
    city.short_description = 'Город'
    city.admin_order_field = 'contact__city'

    def get_level_display(self, obj):
        """Отображение уровня иерархии"""
        return obj.get_level_display_name()
    get_level_display.short_description = 'Уровень'

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request: HttpRequest, queryset: QuerySet):
        """Admin action для очистки задолженности"""
        updated = queryset.update(debt=0)
        self.message_user(
            request,
            f'Задолженность очищена у {updated} объектов.'
        )

    def get_list_filter(self, request):
        """Настройка фильтров"""
        return ['contact__city', 'level', 'created_at']
