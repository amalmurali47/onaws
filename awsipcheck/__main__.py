from . import cli, core

args = cli.parser.parse_args()
args = cli.gather_input(args)

prefixes = core.get_range_prefixes()

core.run(prefixes, args)
