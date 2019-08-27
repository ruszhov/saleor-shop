# Generated by Django 2.1.7 on 2019-04-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0094_auto_20190412_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='product.Category'),
        ),
    ]
