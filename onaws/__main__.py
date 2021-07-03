from . import cli, core, ipranges

def main():
    args = cli.parser.parse_args()
    args = cli.gather_input(args)

    prefixes = ipranges.get_range_prefixes()

    core.run(prefixes, args)


if __name__ == "__main__":
    main()