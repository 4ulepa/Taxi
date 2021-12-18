from django.db import models
from utils.models import generate_unique_slug


class Brand(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=200, default='', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(Brand, self.title)
        super().save(*args, **kwargs)

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
    number = models.CharField(max_length=15, verbose_name='Номер')
    description = models.TextField(max_length=500, default='', blank=True, verbose_name='Описание')
    year = models.PositiveSmallIntegerField(null=True, verbose_name='Год выпуска автомобиля')
    auto_class = models.CharField(max_length=1, choices=AUTO_CLASS_CHOICES, default=AUTO_CLASS_ECONOMY, verbose_name='Класс автомобиля')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, verbose_name='Бренд', related_name='cars')
    options = models.ManyToManyField(Option, related_name='cars')

    def __str__(self):
        return self.number

    def display_engine_power(self):
        return self.pts.engine_power
    display_engine_power.short_description = 'Можность двигателя'

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class VehiclePassport(models.Model):
    auto = models.OneToOneField(Auto, on_delete=models.CASCADE, verbose_name=Auto._meta.verbose_name, related_name='pts')
    vin = models.CharField(max_length=30, verbose_name='Идентификационный номер (VIN)')
    engine_volume = models.SmallIntegerField(verbose_name='Объем двигателя, куб.см')
    engine_power = models.SmallIntegerField(verbose_name='Мощность двигателя, л.с.')

    def __str__(self):
        return f'{self.auto}::{self.vin}'

    class Meta:
        verbose_name = 'Паспорт автомобиля'
        verbose_name_plural = 'Паспорта автомобилей'
