from rest_framework import serializers
import base64
from django.core.files.base import ContentFile

from products.models import Category, Subcategory, Product, ProductImages


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ImagesSerializer(serializers.ModelSerializer):
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
        fields = ('name',
                  'slug',
                  'category',
                  'subcategory',
                  'price',
                  'images')
