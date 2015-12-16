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
def api():
    conf = import_configurations("~/.staccato.conf")['OAuth1Settings']
    api = staccato.startup()
    api.auth(conf["CONSUMER_KEY"], conf["CONSUMER_SECRET"], conf["ACCESS_TOKEN_KEY"], conf["ACCESS_TOKEN_SECRET"])
    return api

