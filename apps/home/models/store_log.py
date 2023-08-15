from django.db import models

class StoreLog(models.Model):

    class Meta:
        ordering = ('store_id', 'timestamp_utc', )

    store_id = models.ForeignKey("Store", related_name="store_log", on_delete=models.CASCADE) # to_field="store_id",
    status = models.CharField(null=True, blank=True, max_length=15)
    timestamp_utc = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)