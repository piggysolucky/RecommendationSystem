import urllib2
from bs4 import BeautifulSoup

#give the input
# Parse the html , and store it in Beautiful Soup format
history = BeautifulSoup(open("/Users/Yn/Documents/CSE5522/Final/History_Page.html"), "lxml")

#test
#print history.prettify()

title=""
#get the names of videos, and add all of them into a long string "title"
for video in history.findAll('a', attrs={'class':'yt-uix-tile-link'}):
    title=title+" "+video.get('title')

#a set that is used to store keywords. 1. Tokenize "title"  2. remove duplicate
name=set(title.split())

#test
print name

