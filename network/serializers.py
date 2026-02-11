from rest_framework import serializers
from .models import NetworkNode, Contact, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'email', 'country', 'city', 'street', 'house_number']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date']


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        source='contact',
        write_only=True
    )
    products = ProductSerializer(many=True, read_only=True)
    products_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='products',
        write_only=True,
        many=True
    )
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        source='supplier',
        allow_null=True,
        write_only=True
    )
    supplier = serializers.StringRelatedField(read_only=True)
    level_display = serializers.CharField(
        source='get_level_display_name',
        read_only=True
    )

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'contact', 'contact_id', 'products', 'products_ids',
            'supplier', 'supplier_id', 'debt', 'level', 'level_display',
            'created_at'
        ]
        read_only_fields = ['debt', 'level', 'created_at']


class NetworkNodeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления без возможности изменения debt"""
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        source='contact'
    )
    products_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='products',
        many=True
    )
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        source='supplier',
        allow_null=True
    )

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'contact_id', 'products_ids',
            'supplier_id', 'debt', 'created_at'
        ]
        read_only_fields = ['debt', 'created_at']

    def validate_supplier_id(self, value):
        """Валидация поставщика для предотвращения циклических ссылок"""
        if value and self.instance:
            if value.id == self.instance.id:
                raise serializers.ValidationError(
                    "Звено сети не может быть своим собственным поставщиком"
                )
        return value

    def create(self, validated_data):
        products = validated_data.pop('products', [])
        node = NetworkNode.objects.create(**validated_data)
        node.products.set(products)
        return node

    def update(self, instance, validated_data):
        products = validated_data.pop('products', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if products is not None:
            instance.products.set(products)

        return instance
