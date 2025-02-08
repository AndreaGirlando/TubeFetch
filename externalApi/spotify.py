
import os
from typing import List
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from externalApi.youtube import fromYoutubeSearchGetLink
load_dotenv()

class PlaylistTracksDTO:
    def __init__(self, id: str, artista: str, canzone: str, numeroTraccia: int, youtubeLink: str, disco: str):
        self.id = id
        self.artista = artista
        self.canzone = canzone
        self.numeroTraccia = numeroTraccia
        self.youtubeLink = youtubeLink
        self.disco = disco
    def __str__(self):
        return f"Track {self.disco}-{self.numeroTraccia}: {self.artista} - {self.canzone} (ID: {self.id}, YouTube: {self.youtubeLink})"

class AlbumInfoDTO:
    def __init__(self, copertina: str, nome: str, dataRilascio: str, artista: str):
        self.copertina = copertina
        self.nome = nome
        self.dataRilascio = dataRilascio
        self.artista = artista

    def __str__(self):
        return f"Album: {self.nome} - {self.artista} (Rilasciato: {self.dataRilascio}, Copertina: {self.copertina})"


def getTracksFromPlaylistUrl(url:str) -> List[PlaylistTracksDTO]:

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_secret = os.getenv('SPOTIPY_CLIENT_SECRET'), client_id= os.getenv('SPOTIPY_CLIENT_ID')))
    album_id = url.split('/')[-1].split("?")[0]

    spotifyPlaylistInfo = sp.album_tracks(album_id=album_id)

    items = []
    try:
        for x in spotifyPlaylistInfo["items"]:
            items.append(PlaylistTracksDTO(
                id=x["id"],
                artista=x["artists"][0]["name"],
                canzone=x["name"],
                numeroTraccia=x["track_number"],
                youtubeLink=os.getenv('YOUTUBE_PREFIX') + fromYoutubeSearchGetLink(x["name"] + " " + x["artists"][0]["name"] + "lyrics"),
                disco=x["disc_number"]
            ))

        return items
    except Exception as e:
        print(e)


def getAlbumInfoFromPlaylistUrl(url:str) -> AlbumInfoDTO:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_secret = os.getenv('SPOTIPY_CLIENT_SECRET'), client_id= os.getenv('SPOTIPY_CLIENT_ID')))
    album_id = url.split('/')[-1].split("?")[0]
    albumInfo = sp.album(album_id=album_id)
    return AlbumInfoDTO(albumInfo["images"][0]["url"], albumInfo["name"], albumInfo["release_date"], albumInfo["artists"][0]["name"])

