'''Simple library to check if a hostname belongs to AWS IP space.'''

__version__ = '0.0.1'

import argparse
import ipaddress
import json
import re
import socket

import requests

AWS_IP_RANGES_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def get_range_prefixes():
    try:
        data = requests.get(AWS_IP_RANGES_URL).json()
    except Exception:
        print('Failed to get IP ranges from AWS')
        return
    else:
        return data['prefixes']


def resolve(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        raise SystemExit(f'Unable to resolve {hostname}. Exiting.')


def generate_s3_hostname(url):
    match = re.search(r'(?:https?)://(\S+\.s3\.amazonaws\.com)', url)
    if match is not None:
        return match.group(1)
    else:
        return '{}.s3.amazonaws.com'.format(url)


def find_prefix(ip):   
    for prefix in prefixes:
        subnet = ipaddress.ip_network(prefix['ip_prefix'])
        if ip_addr in subnet:
            return prefix


def parse_args():
    parser = argparse.ArgumentParser(description='Check if a host belongs to AWS')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-ip", action='store', dest='ip', help="IP to check. Example: 123.123.123.123")
    group.add_argument("-hostname", action='store', dest='hostname', help="Hostname to check. Example: dropbox.s3.amazonaws.com")
    group.add_argument("-bucket", action='store', dest='bucket_name', help="S3 bucket to check. Example: dropbox")
    parser.add_argument('-only-region', action='store_true', dest='only_region', help='Specify this flag to have only region info in the output')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    prefixes = get_range_prefixes()
    
    if args.ip:
        ip = args.ip
        try:
            ip_addr = ipaddress.ip_address(ip)
        except ValueError as e:
            print(e)
        else:
            results = find_prefix(ip_addr)
            if results:
                if args.only_region:
                    print(results['region'])
                else:
                    print(f'{ip} is an AWS IP. Details:')
                    print(json.dumps(results, indent=4))
            else:
                if not args.only_region:
                    print(f'{ip} is not an AWS IP')
                else:
                    print('False')            

    elif args.hostname:
        hostname = args.hostname
        ip = resolve(hostname)
        ip_addr = ipaddress.ip_address(ip)
        results = find_prefix(ip_addr)
        if results:
            if args.only_region:
                print(results['region'])
            else:
                print(f'{hostname} appears to point to an AWS IP. Details:')
                print(json.dumps(results, indent=4))
        else:
            if not args.only_region:
                print(f'{hostname} → {ip_addr} is not an AWS IP')
            else:
                print('False')

    elif args.bucket_name:
        bucket = args.bucket_name
        hostname = generate_s3_hostname(bucket)
        ip = resolve(hostname)
        ip_addr = ipaddress.ip_address(ip)
        print(find_prefix(ip_addr))

