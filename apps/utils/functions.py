import uuid, csv, datetime, os, json, uuid
from django.conf import settings

def custom_id():
    """generates 8 character alphanumeric ID """
    
    # unique_id = secrets.token_urlsafe(8)
    unique_id = str(uuid.uuid4()).replace('-', '')
    return unique_id


# ToDo: Refactor and test properly. Add validations.

# def get_export_filepath(subpath = "", file_prefix = None, file_ext = "txt"):
#     """Returns the filepath for extacting the files"""

#     API_EXPORT_DIR = "AppData/Exports/"
#     today = str(datetime.datetime.today()).replace(":",".")
    
#     if not file_prefix:
#         file_prefix = today

#     date, time = today.split(" ")
#     export_path = "{}/{}".format(API_EXPORT_DIR, date)
    
#     if subpath:
#         export_path = "{}/{}/".format(export_path, subpath.strip('/'))
    
#     export_path = export_path.replace("//", '/')
#     filename = f"{file_prefix}.{file_ext.strip('.')}"

#     if not os.path.isdir(export_path):
#         os.makedirs(export_path)

#     export_filepath = "{}/{}".format(export_path, filename.strip('/'))
#     return filename, export_filepath




# def export_store_report(rid, data):
#     filename, export_filepath = get_export_filepath(
#             subpath="StoreReports",
#             file_prefix=rid,
#             file_ext="csv"
#             )
    
#     with open(export_filepath, 'w', newline='') as data_file:
#         fieldnames = data[0].to_dict().keys()
#         writer = csv.DictWriter(data_file, fieldnames=fieldnames)
#         writer.writeheader()
#         for item in data:
#             writer.writerow(item.to_dict())

#     return filename, export_filepath

    