# Generated by Django 3.2.9 on 2022-03-19 18:27

from django.db import migrations, models
import motorpool.models


class Migration(migrations.Migration):

    dependencies = [
        ('motorpool', '0007_auto_20220319_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=motorpool.models.get_upload_to_auto),
        ),
    ]
