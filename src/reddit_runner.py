#!/usr/bin/env python

from models.reddit import Reddit
import models.db as db
import yaml
import os
from pprint import pprint
import argparse


def main():
    conf = get_configuration()
    subreddit_list = get_subreddit_list(conf)
    r = Reddit(subreddit_list, number_of_links=80)
    get_and_store_entries(r)


def get_configuration():
    current_path = os.path.dirname(__file__)
    f = open(current_path + "/../secrets/config.yaml", "r")
    return yaml.load(f)

def update_db(entries):
    database = db.MongoDB()
    database.put_list_of_entries_to_db(entries)


def get_subreddit_list(conf):
    subreddit_set = set()
    for page in conf['pages'].values():
        subreddit_set.update(page['subreddits'])
    return list(subreddit_set)

def get_and_store_entries(reddit):
    entries = reddit.run()
    print('Pulled entries:' + str(len(entries)))
    update_db(entries)

if __name__ == "__main__":
    main()


