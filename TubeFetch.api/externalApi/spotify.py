
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
    tempYoutubeLink = fromYoutubeSearchGetLink(x["name"] + " " + x["artists"][0]["name"] + "lyrics")
    if tempYoutubeLink != None: tempYoutubeLink = os.getenv('YOUTUBE_PREFIX') + tempYoutubeLink
    temp = TrackDTO(
        id = x["id"],
        artista = x["artists"][0]["name"],
        titolo = x["name"],
        numeroTraccia = x["track_number"],
        youtubeLink = tempYoutubeLink,
        disco = x["disc_number"],
        copertina = x.get("album", {}).get("images", [{}])[0].get("url") if x.get("album", {}).get("images") else None,
    )
    return temp


def get_all_tracks_from_playlist(sp, playlist_id):
    tracks = []
    offset = 0
    while True:
        playlist_tracks = sp.playlist_tracks(playlist_id, offset=offset)
        tracks.extend(playlist_tracks["items"])
        if playlist_tracks["next"] is None:  # Se non ci sono più pagine, esci
            break
        offset += len(playlist_tracks["items"])  # Sposta l'offset per la prossima richiesta
    return tracks

def getPlaylistOrAlbumData(url: str) -> AlbumOrPlaylistInfoDTO:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                                               client_id=os.getenv('SPOTIPY_CLIENT_ID')))
    tracks = []
    if "album" in url:
        album_id = url.split('/')[-1].split("?")[0]
        albumInfo = sp.album(album_id=album_id)
        results = Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(getFormattedDTOfromTrackInfo)(i) for i in albumInfo["tracks"]["items"]
        )
        tracks = [r for r in results if r is not None]
        return AlbumOrPlaylistInfoDTO(albumInfo["images"][0]["url"], albumInfo["name"], albumInfo["release_date"],
                                      albumInfo["artists"][0]["name"], "album", tracks)

    elif "playlist" in url:
        playlist_id = url.split('/')[-1].split("?")[0]
        playlistInfo = sp.playlist(playlist_id=playlist_id)
        all_tracks = get_all_tracks_from_playlist(sp, playlist_id)  # Recupera tutte le tracce
        results = Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(getFormattedDTOfromTrackInfo)(i["track"]) for i in all_tracks if i["track"]  # Evita i None
        )
        tracks = [r for r in results if r is not None]

        return AlbumOrPlaylistInfoDTO(playlistInfo["images"][0]["url"], playlistInfo["name"], None,
                                      playlistInfo["owner"]["display_name"], "playlist", tracks)


def fromSpotifyLinkGetTrackInfo(url:str) -> TrackDTO:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_secret = os.getenv('SPOTIPY_CLIENT_SECRET'), client_id= os.getenv('SPOTIPY_CLIENT_ID')))
    track = sp.track(url.split('/')[-1].split("?")[0])
    res = getFormattedDTOfromTrackInfo(track)
    return res if res else None

def fromIdGetMetadata(id: str):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        client_id=os.getenv('SPOTIPY_CLIENT_ID')
    ))

    try:
        track = sp.track(id)

        metadata = {
            "title": track['name'],
            "artist": ", ".join(artist['name'] for artist in track['artists']),
            "trackNumber": track.get('track_number'),
            "albumArtist": track['album'].get('artists', [{}])[0].get('name'),
            "albumName": track['album'].get('name'),
            "dataRilascio": track['album'].get('release_date'),
            "website": track.get('external_urls', {}).get('spotify'),
            "coverUrl": track['album'].get('images', [{}])[0].get('url')  # highest resolution
        }
    except Exception as e:
        metadata = {}

    return metadata
