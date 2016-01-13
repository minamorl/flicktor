import argparse

from . import *

def subcommand_say(args):
    api().statuses_update(status=args.status)


def subcommand_log(args):
    screen_name = args.screen_name or api().account_verify_credentials()['screen_name']
    logs = api().statuses_user_timeline(screen_name=screen_name)
    for l in logs:
        print_tweet(l)


def subcommand_list(args):
    screen_name = args.screen_name or api().account_verify_credentials()['screen_name']
    logs = api().lists_statuses(count=args.count, slug=args.slug, owner_screen_name=screen_name)
    for l in logs:
        print_tweet(l)


def subcommand_reply(args):
    screen_name = args.screen_name or api().account_verify_credentials()['screen_name']
    logs = api().statuses_mentions_timeline(screen_name=screen_name)
    for l in logs:
        print_tweet(l)


def subcommand_reply(args):
    screen_name = args.screen_name or api().account_verify_credentials()['screen_name']
    logs = api().statuses_mentions_timeline(screen_name=screen_name)
    for l in logs:
        print_tweet(l)


def subcommand_stream(args):
    screen_name = args.screen_name or api().account_verify_credentials()['screen_name']
    for l in api().user_stream():
        if "text" in l:
            print_tweet(l)


def subcommand_remove(args):
    api = api()
    username = args.screen_name or api.account_verify_credentials()['screen_name']

    followers = api.followers_ids(screen_name=username)['ids']
    followings = api.friends_ids(screen_name=username)['ids']

    for user in (api.lookup(str(user) for user in followings if user not in followers)):
        r = api.friendships_destroy(user_id=user['id_str'])
        print(r)


def subcommand_dm(args):
    received_dm = list(api().direct_messages(count=args.count))
    sent_dm = list(api().direct_messages_sent(count=args.count))

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

    api().friendships_create(screen_name=args.screen_name)
    if args.recursive:
        follow_user_recursively(api(), args.screen_name, int(args.count))


def subcommand_search(args):

    tweets = api().search_tweets(q=args.query, count=100).get("statuses")
    for t in tweets:
        print(t.get("text"))



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

    subparser_search = subparsers.add_parser('search')
    subparser_search.add_argument('query', nargs='*', default=None)
    subparser_search.set_defaults(func=subcommand_search)

    subparser_follow = subparsers.add_parser('follow')
    subparser_follow.add_argument('-R', '--recursive', action='store_true', default=False)
    subparser_follow.add_argument('-c', '--count', default=20)
    subparser_follow.add_argument('screen_name', nargs='*', default=None)
    subparser_follow.set_defaults(func=subcommand_follow)

    return parser
