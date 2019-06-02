# SpotiFetch
Download any users Spotify playlist to local Music folder as mp3 ( NO PREMIUM required )

## Description
It is a command line tool that can be used to download mp3 versions of spotify playlists.

## Requirements and Installation Guidelines 
* [youtube_dl](https://github.com/rg3/youtube-dl) :  sudo -H pip3 install --upgrade youtube-dl
* requests : sudo pip3 install requests
* [spotipy](https://github.com/plamere/spotipy) : sudo pip3 install spotipy
* [eyeD3](https://github.com/nicfit/eyeD3) : sudo pip3 install eyeD3
* [google_api_python_client](https://github.com/google/google-api-python-client) : sudo pip3 install --upgrade google-api-python-client

## Usage Steps

* Step 1: Get spotify API key
1. Login with your credentials here: [https://developer.spotify.com/my-applications/#!/](https://developer.spotify.com/my-applications/#!/)
2. Go to My Applications on the sidebar and create an app. Your application name/description does not matter.
3. Your Client ID and Client Secret Keys will be generated.
4. Copy and paste these into "Key.txt"

* Step 2: Open Spotify and find the song/playlist of interest. Click to the 3 dots and then COPY URI

* Step 3: cd into the directory and use 
```
$ python main.py -k key.txt -u <URI>

```

## Useful links to libraries used

* [Spotipy](https://github.com/plamere/spotipy) - Lightweight Python Spotify API
* [EyeD3](https://github.com/nicfit/eyeD3) - Used to edit metadata with Python audio data toolkit (ID3 and MP3)
* [Youtube_dl](https://github.com/rg3/youtube-dl) - Used to download Youtube videos/audio
* [Google_api_python_client](https://github.com/google/google-api-python-client) - Youtube API

## Authors
Manish Shetty M 

## Credits (for finding the problem)
Paromita Roy

