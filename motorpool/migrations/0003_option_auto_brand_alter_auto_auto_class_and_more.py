# Generated by Django 4.0 on 2021-12-09 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motorpool', '0002_auto_20211204_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Опция',
                'verbose_name_plural': 'Опции',
            },
        ),
        migrations.AddField(
            model_name='auto',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='motorpool.brand', verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='auto_class',
            field=models.CharField(choices=[('e', 'Эконом'), ('c', 'Комфорт'), ('b', 'Бизнес')], default='e', max_length=1, verbose_name='Класс автомобиля'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='description',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='number',
            field=models.CharField(max_length=15, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='auto',
            name='year',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Год выпуска автомобиля'),
        ),
        migrations.CreateModel(
            name='VehiclePassport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(max_length=30, verbose_name='Идентификационный номер (VIN)')),
                ('engine_volume', models.SmallIntegerField(verbose_name='Объем двигателя, куб.см')),
                ('engine_power', models.SmallIntegerField(verbose_name='Мощность двигателя, л.с.')),
                ('auto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='motorpool.auto', verbose_name='Автомобиль')),
            ],
            options={
                'verbose_name': 'Паспорт машины',
                'verbose_name_plural': 'Паспорта машин',
            },
        ),
        migrations.AddField(
            model_name='auto',
            name='options',
            field=models.ManyToManyField(to='motorpool.Option'),
        ),
    ]