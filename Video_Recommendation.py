import urllib, json
url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=UCBkNpeyvBO2TdPGVC_PsPUA&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data
