from django.db import models
from apps.utils.functions import custom_id


class StoreReportHeader(models.Model):

    class Status(models.TextChoices):
        RUNNING = "Running"
        COMPLETED = "Completed"
        FAILED = "Failed"

    class Meta:
        ordering = ('-created_on', )

    id = models.CharField(primary_key=True, max_length=25, unique=True, editable=False, default=custom_id)
    status = models.CharField(choices=Status.choices, null=True, blank=True, default=Status.RUNNING, max_length=50)
    filepath = models.CharField(null=True, blank=True, max_length=250)
    created_on = models.DateTimeField(auto_now=True,  null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    def get_report_items(self):
        """Get All Report Items"""
        return self.report_items.all().order_by('store_id')
    
    def to_dict(self):

        dict_obj = {
            "report_id" : self.id,
            "status" : self.status,
            "created_on" : self.created_on
        }

        return dict_obj
    
    @classmethod
    def get_report(cls, id:str) -> object:
        """Get specific Report by ID"""
        try:
            report = cls.objects.get(id=id)
        except Exception as excp:
            print(excp)
            report = None
        return report

class StoreReportItem(models.Model):

    class Meta:
        ordering = ('report_id', )

    id = models.CharField(primary_key=True, max_length=25, unique=True, editable=False, default=custom_id)
    report_id = models.ForeignKey("StoreReportHeader", null=True, blank=True, related_name="report_items", on_delete=models.CASCADE)
    store_id = models.ForeignKey("Store", related_name="store_report", on_delete=models.CASCADE)
    uptime_last_hour = models.IntegerField(null=True, blank=True)
    uptime_last_day = models.IntegerField(null=True, blank=True)
    update_last_week = models.IntegerField(null=True, blank=True)
    downtime_last_hour = models.IntegerField(null=True, blank=True)
    downtime_last_day = models.IntegerField(null=True, blank=True)
    downtime_last_week = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    def to_dict(self):

        dict_obj = {
            "store_id" : self.store_id.id,
            "uptime_last_hour" : self.uptime_last_hour,
            "downtime_last_hour" : self.downtime_last_hour,
            "uptime_last_day" : self.uptime_last_day,
            "downtime_last_day" : self.downtime_last_day,
            "update_last_week" : self.update_last_week,
            "downtime_last_week" : self.downtime_last_week
        }

        return dict_obj


