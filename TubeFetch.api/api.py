import time,os,shutil
from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from externalApi.dto import TrackDTO
from externalApi.spotify import fromSpotifyLinkGetTrackInfo, getPlaylistOrAlbumData
from externalApi.utils import zipAlbumOrPlaylist
from externalApi.youtube import fromYoutubeLinkGetTrackInfo, fromYoutubePlaylistGetInfo
from fileDownload.download import download_mp3

app = Flask(__name__)
CORS(app)
songsPath = "songs"  # Senza backslash errati

@app.route('/rmSongs')
def rmSongs():
    try:
        shutil.rmtree(f"songs",ignore_errors=True)
        return make_response("Ok",200)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)

#! Track endpoint
@app.route('/getSpotifyTrackInfo')
def getSpotifyTrackInfo():
    try:
        spotifyLink = request.args.get("spotifyLink")
        print(spotifyLink)
        res = fromSpotifyLinkGetTrackInfo(spotifyLink)
        if(res == None): return make_response("Canzone non trovata",404)
        return make_response(res.toJson(),200)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)


@app.route('/getYoutubeTrackInfo')
def getYoutubeTrackInfo():
    try:
        youtubeLink = request.args.get("youtubeLink")
        res = fromYoutubeLinkGetTrackInfo(youtubeLink)
        return make_response(res.toJson(),200)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)


@app.route('/downloadOneTrack', methods=['POST'])
def downloadOneTrack():
    try:
        data = request.get_json()
        track = TrackDTO(**data)

        res = download_mp3(track)

        if os.path.isfile(res["filename"]):
            return send_file(os.path.abspath(res["filename"]), as_attachment=True)
        else:
            return make_response(f"File '{res["filename"]}' not found.", 404)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)



#! Album/Playlist endpoints
@app.route('/getSpotifyPlaylistOrAlbumInfo')
def getSpotifyPlaylistOrAlbumInfo():
    try:
        temp = getPlaylistOrAlbumData(request.args.get("spotifyLink"))
        return make_response(temp.toJson(), 200)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)



@app.route('/getYoutubePlaylistOrAlbumInfo')
def getYoutubePlaylistOrAlbumInfo():
    try:
        temp = fromYoutubePlaylistGetInfo(request.args.get("youtubeLink"))
        return make_response(temp.toJson(), 200)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)



@app.route('/downloadSpotifyAlbumOrPlaylist')
def downloadSpotifyAlbumOrPlaylist():
    try:
        uniqueId = str(int(time.time()))
        spotifyLink = request.args.get("spotifyLink")
        if(len(str(spotifyLink)) == 0):
            return make_response(f"Errore",500)
        tempInfo = getPlaylistOrAlbumData(spotifyLink)
        for x in tempInfo.tracks:
            try:
                download_mp3(x, uniqueId)
            except Exception as e:
                print(f"Errore durante il download del brano {x.youtubeLink}: {e}")
            continue


        zipAlbumOrPlaylist(uniqueId)

        res = send_file(os.path.abspath(f"songs/{uniqueId}.zip"))

        shutil.rmtree(f"songs",ignore_errors=True)

        return res
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)


@app.route('/downloadYoutubeAlbumOrPlaylist')
def downloadYoutubeAlbumOrPlaylist():
    try:
        uniqueId = str(int(time.time()))
        youtubeLink = request.args.get("youtubeLink")
        if(len(str(youtubeLink)) == 0):
            return make_response(f"Errore",500)
        tempInfo = fromYoutubePlaylistGetInfo(youtubeLink)
        for x in tempInfo.tracks:
            download_mp3(x, uniqueId)

        zipAlbumOrPlaylist(uniqueId)

        res = send_file(os.path.abspath(f"songs/{uniqueId}.zip"))

        shutil.rmtree(f"songs",ignore_errors=True)

        return res
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)

if __name__ == '__main__':
    shutil.rmtree("songs",ignore_errors=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
