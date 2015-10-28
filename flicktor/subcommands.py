import functools
import configparser
import os
import argparse
import staccato
import clint


def import_configurations(path):
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(path))
    return config


def print_tweet(l):
    clint.textui.puts(clint.textui.colored.cyan("@" + l['user']['screen_name']))
    clint.textui.puts("{} - {} favs".format(l['text'], l['favorite_count']))


def print_direct_message(l):
    clint.textui.puts(clint.textui.colored.cyan("@{} -> @{}".format(l['sender']['screen_name'], l['recipient']['screen_name'])))
    clint.textui.puts("{}".format(l['text']))


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
        print_tweet(l)


def subcommand_list(args):
    screen_name = args.screen_name or _api().account_verify_credentials()['screen_name']
    logs = _api().lists_statuses(count=args.count, slug=args.slug, owner_screen_name=screen_name)
    for l in logs:
        print_tweet(l)


def subcommand_reply(args):
    screen_name = args.screen_name or _api().account_verify_credentials()['screen_name']
    logs = _api().statuses_mentions_timeline(screen_name=screen_name)
    for l in logs:
        print_tweet(l)


def subcommand_reply(args):
    screen_name = args.screen_name or _api().account_verify_credentials()['screen_name']
    logs = _api().statuses_mentions_timeline(screen_name=screen_name)
    for l in logs:
        print_tweet(l)


def subcommand_stream(args):
    screen_name = args.screen_name or _api().account_verify_credentials()['screen_name']
    for l in _api().user_stream():
        if "text" in l:
            print_tweet(l)


def subcommand_remove(args):
    api = _api()
    username = args.screen_name or api.account_verify_credentials()['screen_name']

    followers = api.followers_ids(screen_name=username)['ids']
    followings = api.friends_ids(screen_name=username)['ids']

    for user in (api.lookup(str(user) for user in followings if user not in followers)):
        r = api.friendships_destroy(user_id=user['id_str'])
        print(r)


def subcommand_dm(args):
    for l in _api().direct_messages(count=args.count):
        print_direct_message(l)


def _argpaser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    subparser_say = subparsers.add_parser('say')
    subparser_say.add_argument('status')
    subparser_say.set_defaults(func=subcommand_say)

    subparser_stream = subparsers.add_parser('stream')
    subparser_stream.add_argument('screen_name', nargs='*', default=None)
    subparser_stream.set_defaults(func=subcommand_stream)

    subparser_log = subparsers.add_parser('log')
    subparser_log.add_argument('screen_name', nargs='*', default=None)
    subparser_log.add_argument('-c', '--count', default=None)
    subparser_log.set_defaults(func=subcommand_log)

    subparser_dm = subparsers.add_parser('dm')
    subparser_dm.add_argument('-c', '--count', default=None)
    subparser_dm.set_defaults(func=subcommand_dm)

    subparser_list = subparsers.add_parser('list')
    subparser_list.add_argument('slug')
    subparser_list.add_argument('screen_name', nargs='*', default=None)
    subparser_list.add_argument('-c', '--count', default=None)
    subparser_list.set_defaults(func=subcommand_list)

    subparser_reply = subparsers.add_parser('reply')
    subparser_reply.add_argument('screen_name', nargs='*', default=None)
    subparser_reply.set_defaults(func=subcommand_reply)

    subparser_remove = subparsers.add_parser('remove')
    subparser_remove.add_argument('screen_name', nargs='*', default=None)
    subparser_remove.set_defaults(func=subcommand_remove)

    return parser
