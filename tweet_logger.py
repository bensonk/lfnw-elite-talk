#!/usr/bin/env python
from streaming_twitter import TwitterClient
from sys import argv

def logger(tweet):
  f.write(str(tweet))
  f.write("\n")

client = TwitterClient()
with open(argv[1], 'w') as f:
  client.watch("https://userstream.twitter.com/2/user.json", logger)
