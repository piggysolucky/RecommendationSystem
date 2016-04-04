import urllib2
from bs4 import BeautifulSoup

# give the input
# Parse the html , and store it in Beautiful Soup format
history = BeautifulSoup(open("History_Page.html"), "lxml")

# test
# print history.prettify()


# get the names of videos, and add all of them into a long string "title"
videos = history.findAll('a', attrs={'class': 'yt-uix-tile-link'})
titles = [v.get('title') for v in videos]

# a set that is used to store keywords. 1. Tokenize "title"  2. remove duplicate
name = set(" ".join(titles).split())

# test
print name
