from . import cli, core, ipranges

def main():
    args = cli.parser.parse_args()
    args = cli.gather_input(args)

    try:
        prefixes = ipranges.get_range_prefixes()
    except:
        raise SystemExit('Failed to get AWS IP ranges')
    prefix_tree = core.get_prefix_tree(prefixes)

    core.run(prefix_tree, args)


if __name__ == "__main__":
    main()