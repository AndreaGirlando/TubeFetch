
import multiprocessing
import os
from typing import List
from dotenv import load_dotenv
from joblib import Parallel, delayed
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from externalApi.dto import AlbumOrPlaylistInfoDTO, TrackDTO
from externalApi.youtube import fromYoutubeSearchGetLink
load_dotenv()

def getFormattedDTOfromTrackInfo(x):
    print(x)
    return TrackDTO(
        id=x["id"],
        artista=x["artists"][0]["name"],
        titolo=x["name"],
        numeroTraccia=x["track_number"],
        youtubeLink=os.getenv('YOUTUBE_PREFIX') + fromYoutubeSearchGetLink(x["name"] + " " + x["artists"][0]["name"] + "lyrics"),
        disco=x["disc_number"],
        copertina = x.get("album", {}).get("images", [{}])[0].get("url") if x.get("album", {}).get("images") else None
    )

def getTracksAlbumOrPlaylistUrl(url:str) -> List[TrackDTO]:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_secret = os.getenv('SPOTIPY_CLIENT_SECRET'), client_id= os.getenv('SPOTIPY_CLIENT_ID')))
    idFromUrl = url.split('/')[-1].split("?")[0]
    tempInfo = None
    items = []
    try:
        if("album" in url):
            tempInfo = sp.album_tracks(album_id=idFromUrl)["items"]
            items = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(getFormattedDTOfromTrackInfo)(i) for i in tempInfo)
        elif("playlist" in url):
            tempInfo = sp.playlist_tracks(playlist_id=idFromUrl)["items"]
            items = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(getFormattedDTOfromTrackInfo)(i["track"]) for i in tempInfo)
    except Exception as e:
        print("Errore:" + str(e))
    return items


def getPlaylistOrAlbumData(url:str) -> AlbumOrPlaylistInfoDTO:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_secret = os.getenv('SPOTIPY_CLIENT_SECRET'), client_id= os.getenv('SPOTIPY_CLIENT_ID')))
    tracks = []
    if("album" in url):
        album_id = url.split('/')[-1].split("?")[0]
        albumInfo = sp.album(album_id=album_id)
        tracks = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(getFormattedDTOfromTrackInfo)(i) for i in albumInfo["tracks"]["items"])
        print("XYZ")
        return AlbumOrPlaylistInfoDTO(albumInfo["images"][0]["url"], albumInfo["name"], albumInfo["release_date"], albumInfo["artists"][0]["name"],"album",tracks)
    elif("playlist" in url):
        playlist_id = url.split('/')[-1].split("?")[0]
        playlistInfo = sp.playlist(playlist_id=playlist_id)
        tracks = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(getFormattedDTOfromTrackInfo)(i["track"]) for i in playlistInfo["tracks"]["items"])
        return AlbumOrPlaylistInfoDTO(playlistInfo["images"][0]["url"], playlistInfo["name"], None, playlistInfo["owner"]["display_name"],"playlist",tracks)

def getTrackData(url:str) -> TrackDTO:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_secret = os.getenv('SPOTIPY_CLIENT_SECRET'), client_id= os.getenv('SPOTIPY_CLIENT_ID')))
    track = sp.track(url.split('/')[-1].split("?")[0])
    return getFormattedDTOfromTrackInfo(track)
