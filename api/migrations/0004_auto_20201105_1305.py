# Generated by Django 3.1.2 on 2020-11-05 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_shop_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='img',
            new_name='img_src',
        ),
        migrations.AddField(
            model_name='shop',
            name='google_review_num',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='tabelog_review_num',
            field=models.IntegerField(default=200),
            preserve_default=False,
        ),
    ]