import urllib
import json
#Get top 1000 users on youtube

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