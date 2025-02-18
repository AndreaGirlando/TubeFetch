import datetime

from externalApi.spotify import getPlaylistOrAlbumData, getTracksAlbumOrPlaylistUrl
from fileDownload.download import download_mp3

spotifyPlaylist = "https://open.spotify.com/intl-it/album/1imajJsesRxTvHsI6lErcY?si=L33FcJk4RrmaI4qN3TwKEA"

print("L'album che sto scaricando è il seguente:")
tempInfo = getPlaylistOrAlbumData(spotifyPlaylist)
print(tempInfo)
print("\n\n")


tracks = getTracksAlbumOrPlaylistUrl(spotifyPlaylist)



print("\n\n")
start = datetime.datetime.now()
for x in tracks:
    download_mp3(x.youtubeLink, tempInfo.nome + " - " + tempInfo.artista)
    print("\n\nHo finito di scaricare:")
    print(x)

print(f"\n\n\nLo script ha finito e ci ha messo: {datetime.datetime.now() - start}")






