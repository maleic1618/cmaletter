#!/usr/bin/env python
#!-*-coding:utf-8-*-

from twython import Twython
import webbrowser

CONSUMER_KEY = 'UTjGwUyLUStPp1B956snTQ'
CONSUMER_SECRET = 'VjpEYudF11XSN9vsMeQyycelvQmptHgqqmCmt1eI'

api = Twython(CONSUMER_KEY, CONSUMER_SECRET)
url = api.get_authentication_tokens()
webbrowser.open(url['auth_url'])

verifier = input("PIN code:")
api = Twython(CONSUMER_KEY, CONSUMER_SECRET, url['oauth_token'], url['oauth_token_secret'])
callback = api.get_authorized_tokens(int(verifier))

string = """CONSUMER_KEY = 'UTjGwUyLUStPp1B956snTQ'
CONSUMER_SECRET = 'VjpEYudF11XSN9vsMeQyycelvQmptHgqqmCmt1eI'
ACCESS_KEY = '""" + callback['oauth_token'] +"'\nACCESS_SECRET = '" + callback['oauth_token_secret'] + "'"

with open('secretkey.py', 'w') as f:
    f.write(string)
print("done!")
