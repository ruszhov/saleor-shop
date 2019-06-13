# Generated by Django 2.1.7 on 2019-04-22 11:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0095_auto_20190415_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorytranslation',
            name='seo_title',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.MaxLengthValidator(100)]),
        ),
        migrations.AlterField(
            model_name='collectiontranslation',
            name='seo_title',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.MaxLengthValidator(100)]),
        ),
        migrations.AlterField(
            model_name='producttranslation',
            name='seo_title',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.MaxLengthValidator(100)]),
        ),
    ]
