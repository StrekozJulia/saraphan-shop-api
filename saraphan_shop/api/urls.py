from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet  # ImagesViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('category', CategoryViewSet, basename='categories')
router_v1.register('product', ProductViewSet, basename='products')
# router_v1.register('images', ImagesViewSet, basename='images')

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
