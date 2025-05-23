from datetime import datetime
import pytz

# Date to datetime with timezone
def convert_tz(date):
    return datetime.combine(date, datetime.min.time()).replace(tzinfo=pytz.UTC)

def prep_size(size_str_rep:str, size_type:str):
    # Convert size to appropriate type
    if size_type == 'Percent':
        size_value = float(size_str_rep) / 100.0
    else:
        size_value = float(size_str_rep)
    return size_value