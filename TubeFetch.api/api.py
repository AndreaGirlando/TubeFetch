import time
import shutil
import zipfile
from flask import Flask, request, send_file, make_response
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename

from externalApi.spotify import getPlaylistOrAlbumData, getTrackData, getTracksAlbumOrPlaylistUrl
from externalApi.utils import zipAlbumOrPlaylist
from fileDownload.download import download_mp3

app = Flask(__name__)
CORS(app)
songsPath = "songs"  # Senza backslash errati

#! Track endpoint

@app.route('/getTrackInfo')
def getTrackInfo():
    try:
        spotifyLink = request.args.get("spotifyLink")
        print(spotifyLink)
        res = getTrackData(spotifyLink)
        return make_response(res.toJson(),200)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)

@app.route('/downloadOneTrack')
def downloadOneTrack():
    try:
        uniqueId = str(uuid.uuid1())
        youtubeCode = request.args.get("youtubeCode")
        songName = download_mp3("https://www.youtube.com/watch?v=" + str(youtubeCode), uniqueId) + ".mp3"
        filename = os.path.join(songsPath, uniqueId, songName)

        if os.path.isfile(filename):
            return send_file(os.path.abspath(filename), as_attachment=True)
        else:
            return make_response(f"File '{filename}' not found.", 404)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)

#! Album/Playlist endpoints

@app.route('/getPlaylistOrAlbumInfo')
def getPlaylistOrAlbumInfo():
    try:
        temp = getPlaylistOrAlbumData(request.args.get("spotifyLink"))
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
        tracks = getTracksAlbumOrPlaylistUrl(spotifyLink)
        for x in tracks:
            download_mp3(x.youtubeLink, uniqueId)

        zipAlbumOrPlaylist(uniqueId)

        res = send_file(os.path.abspath(f"songs/{uniqueId}.zip"))

        shutil.rmtree(f"songs",ignore_errors=True)

        return res
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)

if __name__ == '__main__':
    shutil.rmtree("songs",ignore_errors=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
