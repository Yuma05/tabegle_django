from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=128)
    kana = models.CharField(max_length=128)
    place_code = models.CharField(max_length=128)

    def __str__(self):
        return self.name
