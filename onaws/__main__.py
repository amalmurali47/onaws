from . import cli, core, ipranges

def main():
    args = cli.parser.parse_args()
    args = cli.gather_input(args)

    try:
        prefixes = ipranges.get_range_prefixes()
    except:
        raise SystemExit('Failed to get AWS IP ranges')

    core.run(prefixes, args)


if __name__ == "__main__":
    main()