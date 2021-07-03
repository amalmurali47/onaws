import json
import hashlib
from pathlib import Path

import requests

AWS_IP_RANGES_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'

local_data_path = Path('~/.onaws/ip-ranges.json').expanduser()


def get_remote_etag():
    try:
        return requests.head(AWS_IP_RANGES_URL, timeout=10).headers['etag'].strip('"')
    except:
        return None


def get_remote_data():
    return requests.get(AWS_IP_RANGES_URL, timeout=10).text


def get_local_data():
    try:
        return local_data_path.read_text()
    except FileNotFoundError:
        return ""


def save_local_data(data):
    local_data_path.parent.mkdir(parents=True, exist_ok=True)
    local_data_path.write_text(data)


def hexdigest(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def get_range_prefixes():
    data = get_local_data()
    local_digest = hexdigest(data)
    remote_digest = get_remote_etag()
    if local_digest != remote_digest:
        data = get_remote_data()
        save_local_data(data)
    return json.loads(data)['prefixes']
