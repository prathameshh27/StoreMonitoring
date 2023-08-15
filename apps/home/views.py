from django.http import JsonResponse, HttpResponse

from datetime import datetime, timezone
import threading, csv

from .models.store import Store
from .models.report import StoreReportHeader

from .app_utils.functions import *


##########################################################
#                         Views                          #
##########################################################



# API Endpoint: `/api/debug_code/<store_id>`

def debug_code(request, sid):    
    '''Pass a store ID via the endpoint to understand / debug code exection in the console'''

    res = dict()

    max_datetime = datetime.strptime('2023-01-25 18:13:22.479220 UTC', '%Y-%m-%d %H:%M:%S.%f UTC')
    max_datetime_utc = max_datetime.replace(tzinfo=timezone.utc)

    report_obj = StoreReportHeader(status = StoreReportHeader.Status.COMPLETED)

    try:
        store_obj = Store.objects.get(id=sid)
        report = get_store_report(store_obj, max_datetime_utc, report_obj)
        res = report.to_dict()

    except Exception:
        res["error"] = "Something went wrong"


    return JsonResponse(res, safe=False)



# API Endpoint: `/api/trigger_report/`

def run_report(request):    
    """Generates report for every store and returns a report ID"""

    report_obj = StoreReportHeader()
    report_obj.save()

    thread = threading.Thread(target=run_report_task, args=(report_obj,))
    thread.start()

    # asyncio.create_task(async_run_report_task(report_obj))

    res = {
        "ReportID" : report_obj.id
    }

    return JsonResponse(res, safe=False)




# API Endpoint: `/api/get_report/<report_id>`

def get_report(request, rid):
    """Downloads report if available"""

    report = StoreReportHeader.get_report(rid)

    res = {}

    if not report:
        res["error"] = "Invalid Report ID"
        return JsonResponse(res, safe=False)

    if report.status == StoreReportHeader.Status.COMPLETED:

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(report.id)

        writer = csv.writer(response)

        csv_path = report.filepath
        try:
            with open(csv_path, 'r', newline='') as fp:
                reader = csv.reader(fp)
                writer.writerows(reader)
        except Exception:
            res["error"] = "Some error occured while opening the file"
            response = JsonResponse(res, safe=False)

    else:
        res = report.to_dict()
        response = JsonResponse(res, safe=False)

    return response
