#!/usr/bin/env python

import sys
import json

import twitter_utils

t = twitter_utils.login()

def harvest(screen_name):
    max_id = None
    statuses = []
    kwargs = dict(screen_name=screen_name, count=200)

    while True:
        if max_id:
            kwargs["max_id"] = max_id
        
        resp = t.statuses.user_timeline(**kwargs)
        if not resp:
            break
        
        max_id = int(resp[-1]["id"]) - 1
        
        statuses.extend(resp)
        
        print >> sys.stderr, len(statuses), "...",

    return statuses

def pairings():
    statuses = json.load(open("o2-statuses.json"))
    replies = [status for status in statuses if status["in_reply_to_status_id"]]
    pairs = []
    for reply in replies:
        try:
            original = t.statuses.show._(reply["in_reply_to_status_id"])()
        except Exception, e:
            print >> sys.stderr, e
            continue
        pairs.append((original, reply))
        print >> sys.stderr, len(pairs), "...",
    fp = open("pairs.json", "wb")
    json.dump(pairs, fp)
    fp.close()

if __name__ == "__main__":
    statuses = harvest(*sys.argv[1:])
    sys.stdout.write(json.dumps(statuses))
