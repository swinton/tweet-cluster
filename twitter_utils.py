#!/usr/bin/env python

# -*- coding: utf-8 -*-

import os
import sys
import twitter

from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance


def login(token_file=".twitter.oauth"):

    # Go to http://twitter.com/apps/new to create an app and get these items
    # See also http://dev.twitter.com/pages/oauth_single_token

    APP_NAME = 'Mining-the-Social-Web'
    CONSUMER_KEY = 'QlE8MdymSBGZHC79c5pCYA'
    CONSUMER_SECRET = 'nA5J2iIPEm0srw0OpVYqXBjw8AWu2OTk8PIHJE9vkQU'

    try:
        (oauth_token, oauth_token_secret) = read_token_file(token_file)
    except IOError, e:
        (oauth_token, oauth_token_secret) = oauth_dance(APP_NAME, CONSUMER_KEY,
                CONSUMER_SECRET)

        # if not os.path.isdir('out'):
        #     os.mkdir('out')
        
        print >> sys.stderr, "Writing token file"
        write_token_file(token_file, oauth_token, oauth_token_secret)
    
    print >> sys.stderr, "Authenticating"
    return twitter.Twitter(domain='ptt-proxy-nixonmcinnes.apigee.com', api_version='1',
                        auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                        CONSUMER_KEY, CONSUMER_SECRET))

if __name__ == '__main__':
    print "Logging in"
    t = login()
    print getattr(t.statuses.show, "175067192084275200")()
