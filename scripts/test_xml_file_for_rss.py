# Test script to try out and understand RSS feed creation using the rfeed package

import datetime
from rfeed import *

item1 = Item(
    title="First article",
    link="http://www.example.com/articles/1",
    description="This is the description of the first article",
    author="Santiago L. Valdarrama",
    guid=Guid("http://www.example.com/articles/1"),
    pubDate=datetime.datetime(2014, 12, 29, 10, 00))

item2 = Item(
    title="Second article",
    link="http://www.example.com/articles/2",
    description="This is the description of the second article",
    author="Santiago L. Valdarrama",
    guid=Guid("http://www.example.com/articles/2"),
    pubDate=datetime.datetime(2014, 12, 30, 14, 15))

feed = Feed(
    title="Sample RSS Feed",
    link="http://www.example.com/rss",
    description="This is an example of how to use rfeed to generate an RSS 2.0 feed",
    language="en-US",
    lastBuildDate=datetime.datetime.now(),
    items=[item1, item2])

print(feed.rss())

# Try to write the feed variable to file
file = open("test_rss.xml", "w")
file.write(feed.rss())
file.close
# for breakpoint
a = 0
