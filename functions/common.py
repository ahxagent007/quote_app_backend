#from backports.zoneinfo import ZoneInfo
import datetime
import time

#
# def get_current_date_time():
#     return datetime.datetime.now(ZoneInfo("Asia/Dhaka")).strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def current_milli_time():
    return round(time.time() * 1000)

def format_convert_datetime_to_str(date_time_obj):
    date_time_str = str(date_time_obj)
    date_time_str = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%I:%M %p %d-%m-%Y")
    return date_time_str

def convert_from_str(datetime_str):
    datetime_str = time.mktime(datetime_str)
    format = "%b %d %Y %r"
    dateTime = time.strftime(format, time.gmtime(datetime_str))
    return dateTime