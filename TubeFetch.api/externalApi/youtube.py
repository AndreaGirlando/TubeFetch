
import multiprocessing
from joblib import Parallel, delayed
from youtube_search import YoutubeSearch
from pytubefix import Playlist,YouTube

from externalApi.dto import AlbumOrPlaylistInfoDTO, TrackDTO

def getFormattedDTOfromTrackInfo(youtubeLink:str, index:int):
    track = YouTube(youtubeLink)
    return TrackDTO(
        id=track.video_id,
        artista=track.author,
        titolo=track.title.replace("(Official Music Video)",""),
        numeroTraccia=str(index+1),
        youtubeLink=youtubeLink,
        disco="1",
        copertina=track.thumbnail_url,
    )


def fromYoutubeSearchGetLink(search:str):
    temp = YoutubeSearch(search, max_results=1).to_dict()
    return temp[0]["url_suffix"] if temp else None

def fromYoutubePlaylistGetInfo(url:str) -> AlbumOrPlaylistInfoDTO:

    playlist = Playlist(url)
    tracks = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(getFormattedDTOfromTrackInfo)(playlist.video_urls[i],i) for i in range(len(playlist.video_urls)))

    return AlbumOrPlaylistInfoDTO(
        copertina=playlist.thumbnail_url,
        artista=playlist.owner,
        nome=playlist.title,
        dataRilascio="None",
        tipo="playlist",
        tracks=tracks
    )

def fromYoutubeLinkGetTrackInfo(url:str):
    return getFormattedDTOfromTrackInfo(url,1)
