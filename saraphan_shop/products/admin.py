from django.contrib import admin

from .models import Category, Subcategory, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Конфигурация модели Category в админ-панели.
    """
    list_display = ('name', )


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """
    Конфигурация модели Subcategory в админ-панели.
    """
    list_display = ('name', 'category')
    list_filter = ('category', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Конфигурация модели Product в админ-панели.
    """
    list_display = ('name', 'subcategory', 'price')
    list_filter = ('subcategory', 'subcategory__category')
