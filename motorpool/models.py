from django.db import models


class Brand(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['title']  # Сортировка по названию


class Option(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'


class Auto(models.Model):
    AUTO_CLASS_ECONOMY = 'e'
    AUTO_CLASS_COMFORT = 'c'
    AUTO_CLASS_BUSINESS = 'b'

    AUTO_CLASS_CHOICES = (
        (AUTO_CLASS_ECONOMY, 'Эконом'),
        (AUTO_CLASS_COMFORT, 'Комфорт'),
        (AUTO_CLASS_BUSINESS, 'Бизнес'),
    )
    number = models.CharField(max_length=15, name='Номер')
    description = models.TextField(max_length=500, default='', blank=True, name='Описание')
    year = models.PositiveSmallIntegerField(null=True, name='Год выпуска автомобиля')
    auto_class = models.CharField(max_length=1, choices=AUTO_CLASS_CHOICES, default=AUTO_CLASS_ECONOMY, name='Класс автомобиля')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, name='Бренд')
    options = models.ManyToManyField(Option)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
