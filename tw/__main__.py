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

def subcommand_log(args):
    screen_name = args.screen_name or _api().account_verify_credentials()['screen_name']
    logs = _api().statuses_user_timeline(screen_name=screen_name)
    for l in logs:
        print(l['text'])

def import_configurations(path):
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(path))
    return config

def _argpaser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    subparser_say = subparsers.add_parser('say')
    subparser_say.add_argument('status')
    subparser_say.set_defaults(func=subcommand_say)

    subparser_log = subparsers.add_parser('log')
    subparser_log.add_argument('screen_name', nargs='*', default=None)
    subparser_log.set_defaults(func=subcommand_log)

    return parser

if __name__ == '__main__':
    main()
