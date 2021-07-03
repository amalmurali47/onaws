import ipaddress
import json
import re
import socket
import sys
from collections import defaultdict

import requests

AWS_IP_RANGES_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def get_range_prefixes():
    try:
        data = requests.get(AWS_IP_RANGES_URL, timeout=10).json()
    except Exception:
        raise SystemExit('Failed to get IP ranges from AWS')
    else:
        return data['prefixes']


def resolve(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return False


def is_ip(string):
    try:
        return ipaddress.ip_address(string)
    except ValueError:
        return False


def find_prefix(prefixes, ip):
    amz_prefix = None
    non_amz_prefix = None

    # We probably can't rely on the order of prefixes being alphabetical.
    # So try to find any non-AMAZON services with higher precedence.
    # If none found, return the AMAZON service.
    for prefix in prefixes:
        subnet = ipaddress.ip_network(prefix['ip_prefix'])

        if ip in subnet:
            if prefix['service'] == 'AMAZON':
                amz_prefix = prefix
            else:
                non_amz_prefix = prefix
                break

    if non_amz_prefix:
        return non_amz_prefix

    return amz_prefix


def generate_response(result, ip_address=None, hostname=None):
    if result:
        response = {
            'is_aws_ip': True,
            'ip_address': ip_address,
            'service': result['service'],
            'region': result['region'],
            'matched_subnet': result['ip_prefix']
        }
        if hostname:
            response['hostname'] = hostname
    else:
        response = {'is_aws_ip': False}
        
    return response


def process_one(prefixes, host):
    if is_ip(host):
        result = find_prefix(prefixes, ipaddress.ip_address(host))
        response = generate_response(result, ip_address=host)
        return response
    else:
        ip_address = resolve(host)
        if ip_address:
            result = find_prefix(prefixes, ipaddress.ip_address(ip_address))
            response = generate_response(result, hostname=host, ip_address=ip_address)
            return response
        else:
            return {'resolvable': False}


def process(prefixes, args):
    if args['input']:
        return json.dumps(process_one(prefixes, args['input']), indent=4)

    results = defaultdict()
    for host in args['hosts']:
        print(f'Processing: {host}')
        results[host] = process_one(prefixes, host)
    results = json.dumps(dict(results), indent=4)
    print(results)


t_cols = ['is_aws_ip', 'host', 'ip_address', 'service', 'region', 'matched_subnet']


def t_row(host, result):
    row = (str(result.get(col, '')) for col in t_cols)
    return '\t'.join([host, *row])


def j_row(host, result):
    data = {'input': host, **result}
    return json.dumps(data)



def process_stream(prefixes, args):
    func = globals()['{stream}_row'.format_map(args)]

    for host in args['hosts']:
        res = process_one(prefixes, host)
        row = func(host, res)
        print(row)


def run(prefixes, args):
    # print(args['hosts'])
    f = process_stream if args['stream'] else process
    f(prefixes, args)
