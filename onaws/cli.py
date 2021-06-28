import argparse
import sys
from argparse import RawDescriptionHelpFormatter

spec = {
    'description': 'Check if a hostname/IP belongs to AWS',
    'arguments': [
        {
            'options': ['input'],
            'action': 'store',
            'help': 'Input hostname / IP',
            'nargs': '?'
        }
    ],
    'epilog': "Examples:\n\
        onaws 52.219.47.34\n\
        onaws flaws.cloud\n\
        onaws uber.s3.amazonaws.com\n",
    'formatter_class': RawDescriptionHelpFormatter
}

def create_parser(spec):
    parser = argparse.ArgumentParser(
        description=spec['description'],
        epilog=spec['epilog'],
        formatter_class=spec['formatter_class']
    )

    for arg in spec['arguments']:
        options = arg.pop('options', ())
        parser.add_argument(*options, **arg)    
    
    return parser

parser = create_parser(spec)


def stream(inp):
    assert inp is None or isinstance(inp, str)
    return [inp] if inp else iter(sys.stdin)


def sanitize(lines):
    lines = (line.strip() for line in lines)
    return (line for line in lines if line)


def gather_input(args):
    hosts = sanitize(stream(args.input))
    return {
        'input': args.input,
        'hosts': hosts,
    }
