import datetime
from externalApi.spotify import getAlbumInfoFromPlaylistUrl, getTracksFromPlaylistUrl
from fileDownload.download import download_mp3


spotifyPlaylist = "https://open.spotify.com/intl-it/album/5xpkqSPQbp4qTmoaKUHyXp?si=Tk74DxVPQK6GYMaVADqgww"

print("L'album che sto scaricando è il seguente:")
print(getAlbumInfoFromPlaylistUrl(spotifyPlaylist))
print("\n\n")


tracks = getTracksFromPlaylistUrl(spotifyPlaylist)

print("\n\n")
start = datetime.datetime.now()
for x in tracks:
    download_mp3(x.youtubeLink, "1")
    print("\n\nHo finito di scaricare:")
    print(x)

print(f"\n\n\nLo script ha finito e ci ha messo: {datetime.datetime.now() - start}")






