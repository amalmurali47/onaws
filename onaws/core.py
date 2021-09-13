import ipaddress
import json
import socket
import pytricia
import sys

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

def get_prefix_val(prefix_obj):
    try:
        return prefix_obj['ip_prefix']
    except KeyError:
        return prefix_obj['ipv6_prefix']

def get_prefix_tree(prefixes):
    tree = pytricia.PyTricia(128)
    for prefix in prefixes:
        tree[get_prefix_val(prefix)] = prefix
    return tree


def find_prefix(prefix_tree, ip):
    try:
        return prefix_tree[ip]
    except KeyError:
        return None


def generate_response(result, ip_address=None, hostname=None):
    if result:
        response = {
            'is_aws_ip': True,
            'ip_address': ip_address,
            'service': result['service'],
            'region': result['region'],
            'matched_subnet': get_prefix_val(result)
        }
    else:
        response = {
            'is_aws_ip': False,
            'ip_address': ip_address
        }
    if hostname:
        response['hostname'] = hostname
    return response


def process_one(prefix_tree, host):
    if is_ip(host):
        hostname = None
        ip_address = host
    else:
        hostname = host
        ip_address = resolve(host)
        if not ip_address:
            return {'hostname': hostname, 'resolvable': False}

    result = find_prefix(prefix_tree, ip_address)
    return generate_response(result, hostname=hostname, ip_address=ip_address)


def process(prefix_tree, args):
    for host in args['hosts']:
        yield process_one(prefix_tree, host)


def run(prefix_tree, args):
    if args['outfile_path']:
        with open(args['outfile_path'], 'w') as f:
            for result in process(prefix_tree, args):
                f.write(str(result) + '\n')
    else:
        for result in process(prefix_tree, args):
            print(json.dumps(result, indent=4))
