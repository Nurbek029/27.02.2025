from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .choices import OrderStatusEnum

User = get_user_model()

class Category(models.Model):
    title = models.CharField(
        max_length=123,
        verbose_name='Назввание',
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Image(models.Model):
    file = models.ImageField(
        upload_to='media/product_file',
        verbose_name='Файл'
    )

    def __str__(self):
        return str(self.file)
    
    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'

class Product(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=123,
        verbose_name="Название"
        )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='категория'
    )
    main_images = models.ImageField(
        upload_to='media/main_covers',
        verbose_name='Главное фото',
        help_text='Фото которое будет отображаться на альбоме'
    )
    images = models.ManyToManyField(
        Image,
        verbose_name='Изображения'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка'
    )
    comment = models.TextField(
        max_length=500,
        verbose_name='Комментарий'
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user} --> {self.product}'
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class RatingAnswer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    rating = models.ForeignKey(
        Rating,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='rating_answers'
    )
    comment = models.TextField(
        max_length=500,
        verbose_name='Комментарий'
    )
    created_data = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
        )
    update_data = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
        )
    time_limit = models.DateTimeField(
        blank=True,
        null=True,
            verbose_name='Ограничение по времени'
    )

    def __str__(self):
        return f'{self.user} --> {self.rating}'
    
class PaymentMethod(models.Model):
        
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_methods',
        verbose_name='Пользователь'
    )

    title = models.CharField(
        max_length=123,
        verbose_name='Название'
    )

    qr_image = models.ImageField(
        upload_to='media/qr',
        verbose_name='QR'
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'{self.user} --> {self.title}'
    
    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='orders'
    )
    created_data = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    update_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата изменения'
    )
    is_paid = models.BooleanField(
        verbose_name='Принято',
        default=False
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество'
    )
    check_image = models.ImageField(
        verbose_name='Чек',
        upload_to='media/check'
    )
    status = models.CharField(
        choices=OrderStatusEnum.choices,
        default=OrderStatusEnum.IN_PROCESSING,
        verbose_name='Статус оплаты',
        max_length=15
    )
    def __str__(self):
        return f'{self.user} --> {self.product}'
    
    class Meta:
        verbose_name = 'Заявка оплату'
        verbose_name_plural = 'Заявки на оплату'
