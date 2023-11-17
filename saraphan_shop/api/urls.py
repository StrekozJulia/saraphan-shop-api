from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet,
                    ProductInCartViewSet,
                    ProductViewSet,
                    shopping_cart)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('products', ProductViewSet, basename='products')
router_v1.register(r'products/(?P<product_id>\d+)/shopping_cart',
                   ProductInCartViewSet,
                   basename='product_in_cart')

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/shopping_cart', shopping_cart),
    path('v1/', include(router_v1.urls)),
]
