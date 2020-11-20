from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Shop


class UserShop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shops = models.ManyToManyField(Shop)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_shop(sender, instance, created, **kwargs):
    if created:
        UserShop.objects.create(user=instance)
