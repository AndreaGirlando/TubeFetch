from externalApi.spotify import getAlbumInfoFromPlaylistUrl, getTracksFromPlaylistUrl


spotifyPlaylist = "https://open.spotify.com/intl-it/album/5xpkqSPQbp4qTmoaKUHyXp?si=Tk74DxVPQK6GYMaVADqgww"

print(getAlbumInfoFromPlaylistUrl(spotifyPlaylist))

tracks = getTracksFromPlaylistUrl(spotifyPlaylist)

print("\n\n")
for x in tracks:
    print(x)







