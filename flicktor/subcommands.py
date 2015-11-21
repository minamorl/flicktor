import functools
import configparser
import os
import argparse
import staccato
import clint
import datetime
import pytz
import dateutil.parser


def import_configurations(path):
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(path))
    return config


def print_tweet(l):
    created_at = parse_datetime(l['created_at']).strftime('%Y-%m-%d %H:%M:%S')
    clint.textui.puts(clint.textui.colored.cyan("@{} - {}".format(l['user']['screen_name'], created_at)))
    clint.textui.puts("{} - {} favs".format(l['text'], l['favorite_count']))


def print_direct_message(l):
    clint.textui.puts(clint.textui.colored.cyan("@{} -> @{}".format(l['sender']['screen_name'], l['recipient']['screen_name'])))
    clint.textui.puts("{}".format(l['text']))


def parse_datetime(datetime_str):
    return dateutil.parser.parse(datetime_str).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Tokyo'))


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
    received_dm = list(_api().direct_messages(count=args.count))
    sent_dm = list(_api().direct_messages_sent(count=args.count))

    dms = sorted(received_dm + sent_dm, key=lambda dm: parse_datetime(dm["created_at"]), reverse=True)

    for l in dms:
        print_direct_message(l)

def follow_user_recursively(api, username: str, limit: int):
    import time
    followings = api.friends_ids(screen_name=username)['ids']

    for user_id in followings[:limit]:

        print(api.friendships_create(user_id=user_id))
        time.sleep(2)


def subcommand_follow(args):

    _api().friendships_create(screen_name=args.screen_name)
    if args.recursive:
        follow_user_recursively(_api(), args.screen_name, int(args.count))

        


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

    subparser_follow = subparsers.add_parser('follow')
    subparser_follow.add_argument('-R', '--recursive', action='store_true', default=False)
    subparser_follow.add_argument('-c', '--count', default=20)
    subparser_follow.add_argument('screen_name', nargs='*', default=None)
    subparser_follow.set_defaults(func=subcommand_follow)

    return parser
