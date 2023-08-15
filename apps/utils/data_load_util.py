import csv
import pandas as pd

from apps.home.models.store import Store
from apps.home.models.store_hour import StoreHour
from apps.home.models.store_log import StoreLog


"""
Commands:
python manage.py shell
from code_snippets import import_store_statuses
store_data, failure, store_logs = import_store_statuses()
"""

# ToDo: Replace the below functions with django management commands

def import_store():
    """takes the hadcoded csv path as the input and loads all the stores into the database"""

    f = 'Resources/stores.csv'
    with open(f, newline='') as fp:
        stores = []
        reader = csv.reader(fp)
        next(c)
        for row in reader:
            sid, tz = row
            try:
                store = Store(sid, tz)
                stores.append(store)
                print('Passed:', sid)
            except Exception:
                print('Failed:', sid)
        try:
            Store.objects.bulk_create(stores)        
        except Exception as exp:
            print('Insertion Failed:', str(exp))


        
def import_store_hours():
    """takes the hadcoded csv path as the input and loads all the store_hours into the database"""

    f = 'Resources/store_hours.csv'
    with open(f, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        records = []
        failed = []
        for row in csv_reader:
            try:
                row['store_id'] = Store.objects.get(id=row['store_id'])  
                records.append(StoreHour(**row))
            except Exception:
                failed.append(row)
        
        print("Failed:", failed)

        try:
            StoreHour.objects.bulk_create(records)
        except Exception as exp:
            print('Insertion Failed:', str(exp))

    return failed


def import_store_statuses():
    """takes the hadcoded csv path as the input and loads all the store_statuses into the database"""

    f = 'Resources/store_status.csv'
    w = 'Resources/store_status_failures.txt'

    store_data = pd.read_csv(f)

    # store_data = store_data.head(20)

    store_data['timestamp_utc'] = pd.to_datetime(store_data['timestamp_utc'], format='mixed')

    store_data['store_obj'] = store_data['store_id']

    store_logs, failure = [], {}

    for index, row in store_data.iterrows():
        print(str(index).rjust(7,"0"), "\t", row['store_id'])
        try:
            st = Store.objects.get(id=row['store_obj'])
            store_data.at[index, 'store_obj'] = st
            
            log_obj = {
                'store_id': st,
                'status': row['status'],
                'timestamp_utc': row['timestamp_utc']
            }

            try:
                store_logs.append(StoreLog(**log_obj))
            except Exception:
                failure.setdefault("StoreObjFailed", []).append(row['store_obj'])

        except Exception:
            store_data.at[index, 'store_obj'] = None
            failure.setdefault("StoreNotFound", set()).add(row['store_id'])

    try:
        StoreLog.objects.bulk_create(store_logs)
    except Exception as exp:
        print('\n\n\n', 'Final Insertion Failed:', str(exp))

    # valid_data = store_data.dropna(subset=['store_obj']) 
    return store_data, failure, store_logs
