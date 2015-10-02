from tw import subcommands


def main():
    parser = subcommands._argpaser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
