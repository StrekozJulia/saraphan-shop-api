# Generated by Django 4.2.7 on 2023-11-16 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории', max_length=150, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Введите текстовый идентификатор категории', max_length=200, verbose_name='Текстовый идентификатор категории')),
                ('image', models.ImageField(help_text='Вставьте изображение для категории', upload_to='', verbose_name='Иллюстрация категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название продукта', max_length=150, verbose_name='Название продукта')),
                ('slug', models.SlugField(help_text='Введите текстовый идентификатор продукта', max_length=200, verbose_name='Текстовый идентификатор продукта')),
                ('image', models.ImageField(help_text='Вставьте изображение для продукта', upload_to='', verbose_name='Иллюстрация продукта')),
                ('price', models.FloatField(help_text='Введите цену продукта', verbose_name='Цена продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название подкатегории', max_length=150, verbose_name='Название подкатегории')),
                ('slug', models.SlugField(help_text='Введите текстовый идентификатор подкатегории', max_length=200, verbose_name='Текстовый идентификатор подкатегории')),
                ('image', models.ImageField(help_text='Вставьте изображение для подкатегории', upload_to='', verbose_name='Иллюстрация подкатегории')),
                ('category', models.ForeignKey(help_text='Укажите категорию для подкатегории', on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='products.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.CreateModel(
            name='ProductInCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_in_cart', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_in_cart', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_original', models.ImageField(upload_to='', verbose_name='Оригинальная иллюстрация продукта')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='Продукт')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(help_text='Укажите подкатегорию продукта', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.subcategory', verbose_name='Подкатегория'),
        ),
        migrations.AddConstraint(
            model_name='productincart',
            constraint=models.UniqueConstraint(fields=('buyer', 'product'), name='unique_cart_product'),
        ),
    ]
