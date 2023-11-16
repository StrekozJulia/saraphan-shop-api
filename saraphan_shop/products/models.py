from django.db import models
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill

from core.constants import NAME_LEN, SLUG_LEN


class Category(models.Model):
    """Модель категории продукта"""
    name = models.CharField(
        'Название категории',
        help_text='Введите название категории',
        blank=False,
        null=False,
        max_length=NAME_LEN,
    )
    slug = models.SlugField(
        'Текстовый идентификатор категории',
        help_text='Введите текстовый идентификатор категории',
        blank=False,
        null=False,
        max_length=SLUG_LEN
    )
    image = models.ImageField(
        'Иллюстрация категории',
        help_text='Вставьте изображение для категории',
        blank=False,
        null=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    """Модель подкатегории продукта"""
    name = models.CharField(
        'Название подкатегории',
        help_text='Введите название подкатегории',
        blank=False,
        null=False,
        max_length=NAME_LEN,
    )
    slug = models.SlugField(
        'Текстовый идентификатор подкатегории',
        help_text='Введите текстовый идентификатор подкатегории',
        blank=False,
        null=False,
        max_length=SLUG_LEN
    )
    image = models.ImageField(
        'Иллюстрация подкатегории',
        help_text='Вставьте изображение для подкатегории',
        blank=False,
        null=False
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        help_text="Укажите категорию для подкатегории",
        related_name='subcategories',
        blank=False,
        null=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(
        'Название продукта',
        help_text='Введите название продукта',
        blank=False,
        null=False,
        max_length=NAME_LEN,
    )
    slug = models.SlugField(
        'Текстовый идентификатор продукта',
        help_text='Введите текстовый идентификатор продукта',
        blank=False,
        null=False,
        max_length=SLUG_LEN
    )
    image = models.ImageField(
        'Иллюстрация продукта',
        help_text='Вставьте изображение для продукта',
        blank=False,
        null=False,
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        verbose_name='Подкатегория',
        help_text="Укажите подкатегорию продукта",
        related_name='products',
        blank=False,
        null=False
    )
    price = models.FloatField(
        'Цена продукта',
        help_text='Введите цену продукта',
        blank=False,
        null=False,
    )

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        product = self
        ProductImages.objects.create(
            product=Product.objects.get(pk=self.pk),
            image_original=product.image
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductImages(models.Model):
    "Модель с иллюстрациями продукта"
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='images',
        blank=False,
        null=False
    )
    image_original = models.ImageField(
        'Оригинальная иллюстрация продукта',
        blank=False,
        null=False,
    )
    image_small = ImageSpecField(
        [Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(50, 50)],
        source='image_original',
        format='JPEG',
        options={'quality': 90}
    )
    image_medium = ImageSpecField(
        [Adjust(contrast=1.2, sharpness=1.1), ResizeToFit(300, 200)],
        source='image_original',
        format='JPEG',
        options={'quality': 90}
    )
