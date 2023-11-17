from rest_framework import serializers
import base64
from django.core.files.base import ContentFile

from products.models import (Category,
                             Subcategory,
                             Product,
                             ProductImages,
                             ProductInCart,
                             User)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ImagesSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка изображений продукта."""
    image_original = Base64ImageField(required=True, allow_null=True)
    image_small = Base64ImageField(required=True, allow_null=True)
    image_medium = Base64ImageField(required=True, allow_null=True)

    class Meta:
        model = ProductImages
        exclude = ('id', 'product', )


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для отображения подкатегорий внутри категорий."""
    image = Base64ImageField(required=True, allow_null=True)

    class Meta:
        model = Subcategory
        exclude = ('id', 'category', )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для отображения категорий с подкатегориями."""
    image = Base64ImageField(required=True, allow_null=True)
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'image', 'subcategories')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения продуктов."""
    images = ImagesSerializer(many=True)
    category = serializers.ReadOnlyField(source='subcategory.category.name')
    subcategory = serializers.ReadOnlyField(source='subcategory.name')

    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'slug',
                  'category',
                  'subcategory',
                  'price',
                  'images')


class WriteProductInCartSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления продукта в корзину"""

    buyer = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    product = serializers.PrimaryKeyRelatedField(
       read_only=True,
    )

    class Meta:
        model = ProductInCart
        fields = ('buyer', 'product', 'amount',)

    def validate_amount(self, value):
        """Проверка положительности введенного количества товара."""
        if value <= 0:
            raise serializers.ValidationError(
                'Введите положительное число!'
            )
        return value

    def to_representation(self, instance):
        return ReadProductInCartSerializer(instance).data


class ReadProductInCartSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения продуктов в корзине"""

    name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')
    amount = serializers.ReadOnlyField()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.product.price * obj.amount

    class Meta:
        model = ProductInCart
        fields = ('name', 'price', 'amount', 'total_price')


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения корзины с покупками"""
    username = serializers.CurrentUserDefault()
    purchases = ReadProductInCartSerializer(
        many=True,
        source='product_in_cart'
    )
    total_product_names = serializers.SerializerMethodField()
    total_products = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'purchases',
            'total_product_names',
            'total_products',
            'total_price'
        )

    def get_total_product_names(self, obj):
        return obj.product_in_cart.count()

    def get_total_products(self, obj):
        products = obj.product_in_cart.all()
        total_count = 0
        for product in products:
            total_count += product.amount
        return total_count

    def get_total_price(self, obj):
        products = obj.product_in_cart.all()
        total_price = 0
        for product in products:
            total_price += product.amount * product.product.price
        return total_price
