import hashlib
from datetime import datetime


def written_to_snake(string: str) -> str:
    return '_'.join(map(lambda x: x.lower(), string.split()))


def str_to_hex_id(string: str) -> str:
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def fixture_date_to_datetime(date_string: str) -> datetime:
    year_format_length = len(date_string.split('/')[-1])
    if year_format_length == 2:
        return datetime.strptime(date_string, '%d/%m/%y')
    else:
        return datetime.strptime(date_string, '%d/%m/%Y')
