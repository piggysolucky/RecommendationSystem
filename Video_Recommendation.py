import urllib
import json
from bs4 import BeautifulSoup
import requests

userNames = []
#Get top 1000 users on youtube
for pageNum in range(1, 11, 1):
    usersUrl = "http://www.statsheep.com/p/Top-Subscribers?page=" + str(pageNum)
    usersPage = requests.get(usersUrl).text
    soup = BeautifulSoup(usersPage, 'lxml')
    dataTable = soup.find("table", class_="data-table")
    hyperlinks = dataTable.findAll("a")
    for link in hyperlinks:
        userNames += link.contents

#Conver user names to user Id
userIds = []
for userName in userNames:
    url = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername="+userName+"&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
    response = urllib.urlopen(url)
    channelIdInfo = json.loads(response.read())
    items = channelIdInfo["items"]
    userIds += [item["id"] for item in items]


#Get the playlistIds in a channel's playlist
channelPlaylistIds = []
for userId in userIds:
    #url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&forUsername="+userName+"&part=id&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
    url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId="+userId+"&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
    response = urllib.urlopen(url)
    channelPlaylistInfo = json.loads(response.read())
    channelPlaylist = channelPlaylistInfo["items"]
    channelPlaylistIds += [item["id"] for item in channelPlaylist]

#Get the video titles in the playlist
titles = []
for playlistId in channelPlaylistIds:
    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId="+ playlistId + "&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
    response = urllib.urlopen(url)
    channelVideolistInfo = json.loads(response.read())
    videoList = channelPlaylistInfo["items"]
    videoListSnippets = [item["snippet"] for item in videoList]
    titles += [item["title"] for item in videoListSnippets]

print len(titles)