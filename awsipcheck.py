'''Simple library to check if a hostname belongs to AWS IP space.'''

__version__ = '0.0.6'

import argparse
import ipaddress
import json
import re
import socket
import sys
from argparse import RawDescriptionHelpFormatter

import requests

AWS_IP_RANGES_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def get_range_prefixes():
    try:
        data = requests.get(AWS_IP_RANGES_URL).json()
    except Exception:
        print('Failed to get IP ranges from AWS')
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


def is_bucket(string):
    return '.' not in string


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


def parse_args():
    parser = argparse.ArgumentParser(
        description='Check if a hostname/IP belongs to AWS', 
        epilog="Examples:\n\
        awsipcheck 52.219.47.34\n\
        awsipcheck flaws.cloud\n\
        awsipcheck uber.s3.amazonaws.com\n",
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument('input', action='store', help='Input hostname / IP')
    args = parser.parse_args()
    return args


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
        
    return json.dumps(response, indent=4)
    

def main():
    args = parse_args()
    prefixes = get_range_prefixes()

    input_str = args.input

    if input_str:
        if is_ip(input_str):
            result = find_prefix(prefixes, ipaddress.ip_address(input_str))
            response = generate_response(result, ip_address=input_str)
            print(response)
        else:
            ip_address = resolve(input_str)
            if ip_address:                       
                result = find_prefix(prefixes, ipaddress.ip_address(ip_address))
                response = generate_response(result, hostname=input_str, ip_address=ip_address)
                print(response)
            else:
                response = {'resolvable': False}
                print(json.dumps(response, indent=4))        

    
if __name__ == "__main__":
    main()
