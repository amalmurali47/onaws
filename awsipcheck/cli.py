import argparse
import sys

spec = {
    'description': 'Check if a hostname/IP belongs to AWS',
    'arguments': [
        {
            'options': ['input'],
            'action': 'store',
            'help': 'Input hostname / IP',
            'nargs': '?'
        }
    ]
}

def create_parser(spec):
    parser = argparse.ArgumentParser(
        description=spec['description'],
    )

    for arg in spec['arguments']:
        options = arg.pop('options', ())
        parser.add_argument(*options, **arg)    
    
    return parser

parser = create_parser(spec)

def get_raw_input(input_str):
    if input_str is None:
        return sys.stdin.read()

    return input_str


def parse_raw_input(text):
    return [line.strip() for line in text.strip().splitlines() if line.strip()]


def gather_input(args):
    raw = get_raw_input(args.input)
    hosts = parse_raw_input(raw)
    return {
        'input': args.input,
        'hosts': hosts,
    }