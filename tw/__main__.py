import staccato
import argparse
import configparser
import sys
import os
import functools


def main():
    parser = _argpaser()
    args = parser.parse_args()
    args.func(args)


@functools.lru_cache()
def _api():
    conf = import_configurations("~/.staccato.conf")['OAuth1Settings']
    api = staccato.startup()
    api.auth(conf["CONSUMER_KEY"], conf["CONSUMER_SECRET"], conf["ACCESS_TOKEN_KEY"], conf["ACCESS_TOKEN_SECRET"])
    return api

def subcommand_say(args):
    _api().statuses_update(status=args.status)

def import_configurations(path):
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(path))
    return config

def _argpaser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparser_say = subparsers.add_parser('say')
    subparser_say.add_argument('status', )
    subparser_say.set_defaults(func=subcommand_say)

    return parser

if __name__ == '__main__':
    main()
