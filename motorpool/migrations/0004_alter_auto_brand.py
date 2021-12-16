# Generated by Django 4.0 on 2021-12-09 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motorpool', '0003_option_auto_brand_alter_auto_auto_class_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='motorpool.brand', verbose_name='Бренд'),
        ),
    ]