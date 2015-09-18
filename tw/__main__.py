import staccato
import configparser
import sys
import os


def main():
    api = staccato.startup()

    conf = import_configurations("~/.staccato.conf")['OAuth1Settings']
    api.auth(conf["CONSUMER_KEY"], conf["CONSUMER_SECRET"], conf["ACCESS_TOKEN_KEY"], conf["ACCESS_TOKEN_SECRET"])
    api.statuses_update(status=sys.argv[1])


def import_configurations(path):
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(path))
    return config

if __name__ == '__main__':
    main()
