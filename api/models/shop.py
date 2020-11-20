from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=128)
    img_src = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    address = models.CharField(max_length=128)
    tabelog_rating = models.FloatField()
    tabelog_review_num = models.IntegerField()
    google_rating = models.FloatField()
    google_review_num = models.IntegerField()
    total_rating = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_more_one_month(self):
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        if now - self.updated_at > timedelta(days=30):
            return True
        else:
            return False