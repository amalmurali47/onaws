import argparse
import pathlib
import sys
from argparse import RawDescriptionHelpFormatter

spec = {
    'description': 'Check if a hostname/IP belongs to AWS',
    'arguments': [
        {
            'options': ['target'],
            'action': 'store',
            'help': 'Target hostname / IP',
            'nargs': '?'
        },
        {
            'options': ['-i', '--input'],
            'action': 'store',
            'default': None,
            'type': pathlib.Path,
            'help': 'Input file path and name',
        },
        {
            'options': ['-o', '--output'],
            'action': 'store',
            'default': None,
            'type': pathlib.Path,
            'help': 'Output file path and name',
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


def get_raw_input(input_str):
    if input_str is None:
        return sys.stdin
    return [input_str]


def parse_raw_input(text):
    lines = (line.strip() for line in text)
    return (line for line in lines if line)

def check_output_path(outfile_path):
    if outfile_path and not outfile_path.parent.exists():
       print("Output path doesn't exist")
       sys.exit(1)

def check_input_path(infile_path):
    if not infile_path.exists():
       print("Input file doesn't exist")
       sys.exit(1)

def read_input_file(infile_path):
    with open(infile_path, 'r') as f:
        return f.read().splitlines()

def gather_input(args):
    if args.input:
        check_input_path(args.input)
        hosts = read_input_file(args.input)
    else:
        raw = get_raw_input(args.target)
        hosts = parse_raw_input(raw)
    check_output_path(args.output)
    return {
        'hosts': hosts,
        'outfile_path': args.output,
    }
