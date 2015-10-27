from flicktor import subcommands


def main():
    parser = subcommands._argpaser()
    args = parser.parse_args()
    try: 
        args.func(args)
    except AttributeError:
        parser.print_help()


if __name__ == '__main__':
    main()
