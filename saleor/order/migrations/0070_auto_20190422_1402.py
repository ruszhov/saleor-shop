# Generated by Django 2.1.7 on 2019-04-22 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0069_auto_20190225_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='language_code',
            field=models.CharField(default='uk', max_length=35),
        ),
    ]
