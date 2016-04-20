import urllib
import json
url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=UCBkNpeyvBO2TdPGVC_PsPUA&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
response = urllib.urlopen(url)
channelPlaylistInfo = json.loads(response.read())
channelPlaylist = channelPlaylistInfo["items"]
channelSnippets = [item["snippet"] for item in channelPlaylist]
channelTitles = [snippet["title"] for snippet in channelSnippets]
print channelTitles
