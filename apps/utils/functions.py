import uuid, csv, datetime, os, json, uuid
from django.conf import settings

def custom_id():
    """generates 32 character alphanumeric ID """
    
    # unique_id = secrets.token_urlsafe(8)
    unique_id = str(uuid.uuid4()).replace('-', '')
    return unique_id

