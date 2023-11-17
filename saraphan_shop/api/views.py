from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from products.models import Category, Product, ProductInCart
from .serializers import (CategorySerializer,
                          ProductSerializer,
                          ReadProductInCartSerializer,
                          WriteProductInCartSerializer,
                          CartSerializer)
from .permissions import CartPermission


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


class ProductInCartViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticated,
                          CartPermission)

    def get_queryset(self):
        return ProductInCart.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ReadProductInCartSerializer
        return WriteProductInCartSerializer

    def perform_create(self, serializer):
        try:
            amount = int(self.request.data['amount'])
        except KeyError:
            amount = 1

        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        if ProductInCart.objects.filter(buyer=self.request.user,
                                        product=product).exists():
            raise ValidationError(
                'Продукт уже в вашей корзине.'
            )
        serializer.save(buyer=self.request.user,
                        product=product,
                        amount=amount)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        if not ProductInCart.objects.filter(buyer=self.request.user,
                                            product=product).exists():
            raise ValidationError(
                'Продукта нет в вашей корзине.'
            )
        purchase = ProductInCart.objects.get(buyer=self.request.user,
                                             product=product)
        try:
            amount = int(self.request.data['amount'])
        except KeyError:
            amount = 1
        serializer = self.get_serializer(
            instance=purchase,
            data={'amount': amount},
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(methods=['delete'], detail=False)
    def delete(self, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        if not ProductInCart.objects.filter(buyer=self.request.user,
                                            product=product).exists():
            raise ValidationError(
                'Продукта нет в вашей корзине.'
            )
        instance = ProductInCart.objects.filter(buyer=self.request.user,
                                                product=product)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def shopping_cart(request):
    """Просмотр и очистка корзины с покупками"""
    if request.method == 'DELETE':
        cart = request.user.product_in_cart.all()
        cart.delete()
    serializer = CartSerializer(request.user)
    return Response(serializer.data)
