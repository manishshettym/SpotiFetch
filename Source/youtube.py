from __future__ import unicode_literals

# youtube api
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# youtube-dl
import youtube_dl

# metatags
import eyed3

# import
from unicodedata import normalize
import requests
import os

eyed3.log.setLevel("ERROR")

# YOUTUBE API
def set_yids(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, DEVELOPER_KEY):
    yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY, cache_discovery=False)
    return yt

def youtube_search(yt, search, max_results = 3):
    search_response = yt.search().list(
        q=search,
        part="id,snippet",
        maxResults=max_results
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"].encode("utf-8")
            idn = search_result["id"]["videoId"].encode("utf-8")
            videos.append({idn: title})

    return videos

def youtubedl(yt, s_list, metadata, pl_dir, songlistdir, audioquality):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,
        'outtmpl': pl_dir + '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': audioquality,
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for song, data in zip(s_list, metadata):
            a = str(normalize('NFKD', song[0]).encode('ascii','ignore'))[2:-1]
            t = str(normalize('NFKD', song[len(song)-1]).encode('ascii','ignore'))[2:-1]
            # print(a , t , " IS THE QUERY")

            ytid_l = youtube_search(yt, [a, t])

            if not ytid_l:
                continue
            else: # Post Check videos (expand with function later)
                print(song , "was found")
                for vid in ytid_l:
                    vid_keys = list(vid.keys())
                    link = ["http://www.youtube.com/watch?v=" + str(vid_keys[0])[2:-1]]
                    info_dict = ydl.extract_info(link[0], download=False)
                    duration = info_dict.get("duration", None)
                    if duration < 60*15:
                        ytid = vid
                        break

            path = pl_dir + ', '.join(data[4]).replace('/', '') + " - " + data[0].replace('/', '') + ".mp3"
            removepath = pl_dir + str(list(ytid.keys())[0])[2:-1] + ".mp3"

            flag_d = True
            try:
                ydl.download(link)
            except:
                flag_d = False
                pass

            if(flag_d == False):
                print("Could not Download")
                continue

            response = requests.get(data[2].encode("utf-8")).content
            temppng = pl_dir + 'cover.png'
            with open(temppng, 'wb') as handler:
                handler.write(response)

            img = open(temppng,"rb").read()

            # metadata.extend([title, album, coverart, track_nom, artists, genre, idnom])
            audiofile = eyed3.load(removepath)
            audiofile.tag.artist = u'' + ', '.join(data[4])
            audiofile.tag.album = u'' + data[1]
            audiofile.tag.album_artist = u'' + ', '.join(data[4])
            audiofile.tag.title = u'' + data[0]
            audiofile.tag.track_num = data[3]
            audiofile.tag.genre = u'' + str(data[5])[2:-1]
            imgframe = audiofile.tag.images.set(3, img, "image/jpeg")
            audiofile.tag.save()

            os.rename(removepath, path)
            os.remove(temppng)
            if not os.path.isfile(songlistdir):
                f= open(songlistdir,"w+")
                f.close()

            with open(songlistdir, "a") as f:
                f.write(str(data[6])[2:-1])
                f.write("\n")

            print (str(t)[2:-1] + "\t" + "Song downloaded")
