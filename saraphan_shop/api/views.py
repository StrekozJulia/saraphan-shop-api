from rest_framework import permissions, viewsets

from products.models import Category, Product, ProductImages
from .serializers import CategorySerializer, ProductSerializer, ImagesSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Просмотр имеющихся категорий продуктов"""

    http_method_names = ('get', )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    """Просмотр имеющихся категорий продуктов"""

    http_method_names = ('get', )
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ImagesViewSet(viewsets.ModelViewSet):
    """Просмотр имеющихся категорий продуктов"""

    http_method_names = ('get', )
    serializer_class = ImagesSerializer
    queryset = ProductImages.objects.all()
