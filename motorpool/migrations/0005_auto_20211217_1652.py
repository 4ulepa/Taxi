# Generated by Django 3.2.9 on 2021-12-17 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motorpool', '0004_alter_auto_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='auto',
            name='options',
            field=models.ManyToManyField(related_name='cars', to='motorpool.Option'),
        ),
        migrations.AlterField(
            model_name='vehiclepassport',
            name='auto',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pts', to='motorpool.auto', verbose_name='Автомобиль'),
        ),
    ]
