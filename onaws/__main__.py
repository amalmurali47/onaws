from . import cli, core

def main():
    args = cli.parser.parse_args()
    args = cli.gather_input(args)

    prefixes = core.get_range_prefixes()

    core.run(prefixes, args)


if __name__ == "__main__":
    main()