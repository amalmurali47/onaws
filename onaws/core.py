import ipaddress
import json
import socket

import requests

AWS_IP_RANGES_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def get_range_prefixes():
    try:
        data = requests.get(AWS_IP_RANGES_URL, timeout=10).json()
    except Exception:
        raise SystemExit('Failed to get IP ranges from AWS')
    return data['prefixes']


def resolve(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def is_ip(string):
    try:
        return bool(ipaddress.ip_address(string))
    except ValueError:
        return False


def find_prefix(prefixes, ip):
    result_prefix = None

    # We probably can't rely on the order of prefixes being alphabetical.
    # So try to find any non-AMAZON services with higher precedence.
    # If none found, return the AMAZON service.
    for prefix in prefixes:
        subnet = ipaddress.ip_network(prefix['ip_prefix'])
        if ip in subnet:
            result_prefix = prefix
            if prefix['service'] != 'AMAZON':
                break

    return result_prefix


def generate_response(result, ip_address=None, hostname=None):
    if result:
        response = {
            'is_aws_ip': True,
            'ip_address': ip_address,
            'service': result['service'],
            'region': result['region'],
            'matched_subnet': result['ip_prefix']
        }
    else:
        response = {
            'is_aws_ip': False,
            'ip_address': ip_address
        }
    if hostname:
        response['hostname'] = hostname
    return response


def process_one(prefixes, host):
    if is_ip(host):
        hostname = None
        ip_address = host
    else:
        hostname = host
        ip_address = resolve(host)
        if not ip_address:
            return {'hostname': hostname, 'resolvable': False}

    result = find_prefix(prefixes, ipaddress.ip_address(ip_address))
    return generate_response(result, hostname=hostname, ip_address=ip_address)


def process(prefixes, args):
    for host in args['hosts']:
        yield json.dumps(process_one(prefixes, host), indent=4)


def run(prefixes, args):
    for result in process(prefixes, args):
        print(result)
