# Generated by Django 3.1.2 on 2020-11-06 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201105_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='address',
            field=models.CharField(default='tokyo', max_length=128),
            preserve_default=False,
        ),
    ]