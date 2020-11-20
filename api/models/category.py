from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)
    kana = models.CharField(max_length=128)
    category_code = models.CharField(max_length=128)

    def __str__(self):
        return self.name
