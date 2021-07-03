import ipaddress
import json
import socket
import pytricia


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


def get_prefix_tree(prefixes):
    tree = pytricia.PyTricia()
    for prefix in prefixes:
        tree[prefix["ip_prefix"]] = prefix
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
        yield json.dumps(process_one(prefix_tree, host), indent=4)


def run(prefix_tree, args):
    for result in process(prefix_tree, args):
        print(result)
