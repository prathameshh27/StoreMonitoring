from django.db import models


class Day(models.IntegerChoices):
    Monday    = 0, 'Monday'
    Tuesday   = 1, 'Tuesday'
    Wednesday = 2, 'Wednesday'
    Thursday  = 3, 'Thursday'
    Friday    = 4, 'Friday'
    Saturday  = 5, 'Saturday'
    Sunday    = 6, 'Sunday'


class StoreHour(models.Model):

    class Meta:
        ordering = ('store_id', 'dayOfWeek', )

    store_id = models.ForeignKey("Store", related_name="store_hours", on_delete=models.CASCADE) #to_field="store_id"
    dayOfWeek = models.IntegerField(null=True, blank=True, choices=Day.choices)
    start_time_local = models.TimeField(null=True, blank=True)
    end_time_local = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
