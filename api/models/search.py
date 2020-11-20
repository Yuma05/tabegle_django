from django.db import models
from api.models import Shop


class Search(models.Model):
    place_code = models.CharField(max_length=128, blank=True)
    category_code = models.CharField(max_length=128, blank=True)
    shops = models.ManyToManyField(Shop)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.place_code

    def is_more_one_month(self):
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        if now - self.updated_at > timedelta(days=30):
            return True
        else:
            return False
