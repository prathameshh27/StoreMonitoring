import uuid, csv, os, pytz
from concurrent.futures import ThreadPoolExecutor

from ..models.store import Store
from ..models.report import StoreReportHeader, StoreReportItem

from datetime import datetime, timezone, timedelta


def custom_id():
    """generates 32 character alphanumeric ID """
    
    # unique_id = secrets.token_urlsafe(8)
    unique_id = str(uuid.uuid4()).replace('-', '')
    return unique_id




# ToDo: Refactor and test properly. Add validations.

def get_export_filepath(subpath = "", file_prefix = None, file_ext = "txt"):
    """Returns the filepath for extacting the files"""

    API_EXPORT_DIR = "AppData/Exports/"
    today = str(datetime.today()).replace(":",".")
    
    if not file_prefix:
        file_prefix = today

    date, time = today.split(" ")
    export_path = "{}/{}".format(API_EXPORT_DIR, date)
    
    if subpath:
        export_path = "{}/{}/".format(export_path, subpath.strip('/'))
    
    export_path = export_path.replace("//", '/')
    filename = f"{file_prefix}.{file_ext.strip('.')}"

    if not os.path.isdir(export_path):
        os.makedirs(export_path)

    export_filepath = "{}/{}".format(export_path, filename.strip('/'))
    return filename, export_filepath




def export_store_report(rid, data):
    filename, export_filepath = get_export_filepath(
            subpath="StoreReports",
            file_prefix=rid,
            file_ext="csv"
            )
    try:
        with open(export_filepath, 'w', newline='') as data_file:
            fieldnames = data[0].to_dict().keys()
            writer = csv.DictWriter(data_file, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(item.to_dict())

    except Exception:
        filename, export_filepath = None, None

    return filename, export_filepath

    


##########################################################
#              Helper Functions for views                #
##########################################################



def get_days(start, step):
    """Returns a list with indices for the days found within input range"""

    days = []
    
    for r in range(0, step+1):
        day = (start + r) % 7
        if day not in days:
            days.append(day)
    
    return days  



def get_timedelta_in_mins(start, end):
    """Returns time delta in minutes"""
    diff = end - start
    diff_mins = diff.total_seconds() / 60
    return round(diff_mins, 2)



# Refer to the README.md file for the logic 

def process_logs(store_logs, int_start_pt, int_end_pt):
    """This fuction does an analysis on the logs found in the valid interval to calculate the possible uptime / downtime"""
    log_objs = store_logs.filter(timestamp_utc__range=(int_start_pt, int_end_pt)).order_by('timestamp_utc')
    
    # ftr_logs = ftr_logs | log_objs if ftr_logs else log_objs 
    
    timeframe_downtime_mins = 0
    downtime_start, downtime_end = None, None

    timeframe_in_mins = get_timedelta_in_mins(int_start_pt, int_end_pt)

    print("Below are the logs from the applicable / searchable interval:", end="\n\n")
    is_active = False
    for log in log_objs:
        print("Log:", log.status, log.timestamp_utc, sep="\t\t", end="\n\n")
        
        if log.status == "inactive" and downtime_start == None:
            downtime_start = log.timestamp_utc

        if log.status == "active":
            is_active = False
            if downtime_start != None:
                downtime_end = log.timestamp_utc
                timeframe_downtime_mins += get_timedelta_in_mins(downtime_start, downtime_end)
                downtime_start, downtime_end = None, None

    if downtime_start != None:
        timeframe_downtime_mins += get_timedelta_in_mins(downtime_start, int_end_pt)
        downtime_start, downtime_end = None, None

    timeframe_uptime_mins = abs(timeframe_in_mins - timeframe_downtime_mins)

    # if the store is not found active then check if the uptime is greater than 10% of the store operating hours
    # if not then return 0 
    if not is_active:
        timeframe_uptime_mins = timeframe_uptime_mins if (timeframe_uptime_mins / timeframe_in_mins) * 100 > 10 else 0

    return timeframe_uptime_mins, timeframe_downtime_mins



# Refer to the README.md file for the logic 

def get_activity_in_mins(store_obj, max_datetime_utc, min_datetime_utc):
    """Accepts an interval and retrives uptime and downtime in the previously specified period."""
    
    print("+"*90, end='\n\n')
    
    max_day = max_datetime_utc.weekday()

    store_tz_str = store_obj.timezone_str
    store_tz = pytz.timezone(store_tz_str)

    store_hrs = store_obj.store_hours.all().order_by('dayOfWeek')
    store_logs = store_obj.store_log.all()

    int_start_pt, int_end_pt = min_datetime_utc, max_datetime_utc

    print("Input Timeframe (Hr, Day, Week):", int_start_pt, int_end_pt, sep="\t\t", end="\n\n")

    int_delta = int_end_pt - int_start_pt

    int_sday = int_start_pt.weekday()
    int_step = int_delta.days
    days = get_days(int_sday, int_step)      

    print("Interval & Days to look for:", int_step, days, '\n', sep='\t')

    ftr_store_hrs = store_hrs.filter(dayOfWeek__in=days)

    ftr_logs = None

    total_uptime, total_downtime = 0,0

    print("Below are the Operating hours for the store: ", store_obj.id, "\n")
    
    if ftr_store_hrs:
        for hours in ftr_store_hrs:
            print("-"*50, end="\n\n")

            int_start_pt, int_end_pt = min_datetime_utc, max_datetime_utc

            day_offset = (max_day - hours.dayOfWeek) % 7
            curr_date = max_datetime_utc.date() - timedelta(days=day_offset)

            start_dt = store_tz.localize(datetime.combine(curr_date, hours.start_time_local))
            end_dt = store_tz.localize(datetime.combine(curr_date, hours.end_time_local))

            print("Day of the week:", hours.dayOfWeek, end="\n\n")

            print("Local Interval:", start_dt, end_dt, sep="\t\t", end="\n\n")

            start_datetime_utc = start_dt.astimezone(pytz.utc)
            end_datetime_utc = end_dt.astimezone(pytz.utc)

            print("UTC Interval:", start_datetime_utc, end_datetime_utc, sep="\t\t", end="\n\n")

            # Checks the overlap between operating hours and input interval / timeframe
            if (int_start_pt <= start_datetime_utc <= int_end_pt
                or int_start_pt <= end_datetime_utc <= int_end_pt
                or start_datetime_utc <= int_start_pt <= end_datetime_utc
                or start_datetime_utc <= int_end_pt <= end_datetime_utc):

                int_start_pt = max(int_start_pt, start_datetime_utc)
                int_end_pt = min(int_end_pt, end_datetime_utc)

                print("Valid/applicable Interval:", int_start_pt, int_end_pt, sep="\t\t", end="\n\n")
                print("."*20, end="\n\n")

                timeframe_uptime_mins, timeframe_downtime_mins = process_logs(store_logs, int_start_pt, int_end_pt)

                total_uptime += timeframe_uptime_mins
                total_downtime += timeframe_downtime_mins

                print("."*20, end="\n\n")
                print("Local Timeframe - Uptime / Downtime:", timeframe_uptime_mins, timeframe_downtime_mins, sep="\t\t", end="\n\n")

    else:
        timeframe_uptime_mins, timeframe_downtime_mins = process_logs(store_logs, int_start_pt, int_end_pt)

        total_uptime += timeframe_uptime_mins
        total_downtime += timeframe_downtime_mins

        print("."*20, end="\n\n")
        print("Local Timeframe - Uptime / Downtime:", timeframe_uptime_mins, timeframe_downtime_mins, sep="\t\t", end="\n\n")


    total_uptime = round(total_uptime, 2)        
    total_downtime = round(total_downtime, 2) 

    print("-"*50, end="\n\n")
    print("Input Timeframe (aggregated) - Uptime / Downtime:", total_uptime, total_downtime, sep="\t\t", end="\n\n")
    
    print("-"*50, end="\n\n")
    return total_uptime, total_downtime



def get_store_report(store_obj, max_datetime_utc, report_obj=0) -> dict:
    """Handles a single instance of a store and retrive the uptime and downtime in - past_hour, past_day, past_week"""

    past_hour_utc = max_datetime_utc - timedelta(hours=1)
    past_day_utc  = max_datetime_utc - timedelta(days=1)
    past_week_utc = max_datetime_utc - timedelta(days=7)

    uptime_lh, downtime_lh = get_activity_in_mins(store_obj, max_datetime_utc, past_hour_utc)
    uptime_ld, downtime_ld = get_activity_in_mins(store_obj, max_datetime_utc, past_day_utc)
    uptime_lw, downtime_lw = get_activity_in_mins(store_obj, max_datetime_utc, past_week_utc)

    uptime_ld, downtime_ld = round(uptime_ld/60), round(downtime_ld/60)
    uptime_lw, downtime_lw = round(uptime_lw/60), round(downtime_lw/60)

    json_res = {
        "report_id" : report_obj,
        "store_id" : store_obj,
        "uptime_last_hour" : uptime_lh,
        "downtime_last_hour" : downtime_lh,
        "uptime_last_day" : uptime_ld,
        "downtime_last_day" : downtime_ld,
        "update_last_week" : uptime_lw,
        "downtime_last_week" : downtime_lw
    }

    rep_item = StoreReportItem(**json_res)

    return rep_item




def run_report_task(report_obj):
    """Takes in Report object and executes parallel threads to process result"""

    max_datetime = datetime.strptime('2023-01-25 18:13:22.479220 UTC', '%Y-%m-%d %H:%M:%S.%f UTC')
    max_datetime_utc = max_datetime.replace(tzinfo=timezone.utc)

    store_reports = []
    all_stores = Store.objects.all()[:100]

    max_threads = 4

    def populate_store_report(store_obj):
        report = get_store_report(store_obj, max_datetime_utc, report_obj)
        store_reports.append(report)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for store_obj in all_stores:
            executor.submit(populate_store_report, store_obj)

    executor.shutdown()

    try:
        StoreReportItem.objects.bulk_create(store_reports)
        status = StoreReportHeader.Status.COMPLETED
    except Exception:
        status = StoreReportHeader.Status.FAILED


    filename, export_filepath = export_store_report(rid=report_obj.id, data=store_reports)

    report_obj.status = status
    report_obj.filepath = export_filepath
    report_obj.save()
