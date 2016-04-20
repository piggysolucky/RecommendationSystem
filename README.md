# RecommendationSystem
AI project for CSE5522; Implementation of a simple video recommendation system
Retrive channel playId
1 Create a google app api key which has credentials for Youtube data API V3:AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE, see instructions on youtuve data API
See reference for how to use Youtuve Data API:https://developers.google.com/youtube/v3/getting-started

2 See reference for the Hppt request parameters :
http://stackoverflow.com/questions/26831919/get-all-playlist-ids-from-channel-id-youtube-api-v3
https://developers.google.com/youtube/v3/docs/playlists/list#parameters
playlistitem:
https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=PLB03EA9545DD188C3&key=MY_API_KEY

basically use https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=UCBkNpeyvBO2TdPGVC_PsPUA&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE
(api key is the key above), we can retrive the api key of a channel
－－－－－－－－－－

