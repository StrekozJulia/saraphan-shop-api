from rest_framework import mixins, viewsets


class ProductMixin(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    pass
