from django.db import models

class Store(models.Model):
    # store_id = models.CharField(null=True, unique=True, blank=True, max_length=50)
    timezone_str = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return str(self.id)

