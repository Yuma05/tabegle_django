# Generated by Django 3.1.2 on 2020-11-07 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_shop_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
