# Generated by Django 3.1.2 on 2020-11-09 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_search_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('kana', models.CharField(max_length=128)),
                ('place_code', models.CharField(max_length=128)),
            ],
        ),
    ]
