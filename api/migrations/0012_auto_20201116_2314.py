# Generated by Django 3.1.2 on 2020-11-16 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20201116_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='category_code',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='search',
            name='place_code',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
