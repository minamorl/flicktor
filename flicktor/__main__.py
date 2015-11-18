from flicktor import subcommands


def main():
    parser = subcommands._argpaser()
    args = parser.parse_args()
    try: 
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()


    except KeyboardInterrupt:
        print("bye.")


if __name__ == '__main__':
    main()
