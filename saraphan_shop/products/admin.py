from django.contrib import admin

from .models import Category, Subcategory, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Конфигурация модели Category в админ-панели.
    """
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """
    Конфигурация модели Subcategory в админ-панели.
    """
    list_display = ('name', 'category')
    search_fields = ('name', )
    list_filter = ('category', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Конфигурация модели Product в админ-панели.
    """
    list_display = ('name', 'subcategory', 'price')
    search_fields = ('name', )
    list_filter = ('subcategory', 'subcategory__category')
