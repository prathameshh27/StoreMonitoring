from django.contrib import admin

from .models.store import Store
from .models.store_hour import StoreHour
from .models.store_log import StoreLog
from .models.report import StoreReportHeader, StoreReportItem

# Register your models here.

class AdminStore(admin.ModelAdmin):
    list_display = ['id', 'timezone_str']    

class AdminStoreHour(admin.ModelAdmin):
    list_display = ['id', 'store_id', 'dayOfWeek', 'start_time_local', 'end_time_local']

class AdminStoreLog(admin.ModelAdmin):
    list_display = ['id', 'store_id', 'status', 'timestamp_utc']

class AdminStoreReportHeader(admin.ModelAdmin):
    list_display = ['id', 'filepath', 'status', 'created_on']

class AdminStoreReportItem(admin.ModelAdmin):
    list_display = ['id', 'store_id', 'uptime_last_hour', 'uptime_last_day', 'update_last_week', 'downtime_last_hour', 'downtime_last_day', 'downtime_last_week', 'report_id']


admin.site.register(Store, AdminStore)
admin.site.register(StoreHour, AdminStoreHour)
admin.site.register(StoreLog, AdminStoreLog)
admin.site.register(StoreReportHeader, AdminStoreReportHeader)
admin.site.register(StoreReportItem, AdminStoreReportItem)