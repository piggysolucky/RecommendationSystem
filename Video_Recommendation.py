import urllib
import json
from bs4 import BeautifulSoup
import requests

userIDs = []
#Get top 1000 users on youtube
for pageNum in range(1, 11, 1):
    usersUrl = "http://www.statsheep.com/p/Top-Subscribers?page=" + str(pageNum)
    usersPage = requests.get(usersUrl).text
    soup = BeautifulSoup(usersPage, 'lxml')
    dataTable = soup.find("table", class_="data-table")
    hyperlinks = dataTable.findAll("a")
    for link in hyperlinks:
        userIDs += link.contents
print len(userIDs)

#Get the playlistIds in a channel's playlist
url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=UCBkNpeyvBO2TdPGVC_PsPUA&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
response = urllib.urlopen(url)
channelPlaylistInfo = json.loads(response.read())
channelPlaylist = channelPlaylistInfo["items"]
channelPlaylistIds = [item["id"] for item in channelPlaylist]

#Get the video titles in the playlist
titles = []
for playlistId in channelPlaylistIds:
    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId="+ playlistId + "&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
    response = urllib.urlopen(url)
    channelVideolistInfo = json.loads(response.read())
    videoList = channelPlaylistInfo["items"]
    videoListSnippets = [item["snippet"] for item in videoList]
    titles += [item["title"] for item in videoListSnippets]

print titles