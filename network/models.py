from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Contact(models.Model):
    """Модель контактов"""
    email = models.EmailField(max_length=254, verbose_name='Email', unique=True)
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=20, verbose_name='Номер дома')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street} {self.house_number}"


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    """Модель звена сети"""
    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='network_nodes',
        verbose_name='Контакты'
    )
    products = models.ManyToManyField(
        Product,
        related_name='network_nodes',
        verbose_name='Продукты'
    )
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='network_nodes',
        verbose_name='Поставщик'
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Задолженность перед поставщиком'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        default=0,
        editable=False,
        verbose_name='Уровень иерархии'
    )

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Автоматическое определение уровня иерархии"""
        if self.supplier:
            self.level = self.supplier.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)

    def get_level_display_name(self):
        """Получение отображаемого названия уровня"""
        return dict(self.LEVEL_CHOICES).get(self.level, "Неизвестный уровень")
