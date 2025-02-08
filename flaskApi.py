from flask import Flask, send_file, make_response
import os
import uuid
from werkzeug.utils import secure_filename

from fileDownload.download import download_mp3

app = Flask(__name__)
songsPath = "songs"  # Senza backslash errati

@app.route('/downloadOneTrack/<youtubeCode>')
def downloadOneTrack(youtubeCode):
    try:
        uniqueId = str(uuid.uuid1())
        songName = download_mp3("https://www.youtube.com/watch?v=" + str(youtubeCode), uniqueId) + ".mp3"
        filename = os.path.join(songsPath, uniqueId, songName)

        if os.path.isfile(filename):
            return send_file(os.path.abspath(filename), as_attachment=True)
        else:
            return make_response(f"File '{filename}' not found.", 404)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)

if __name__ == '__main__':
    app.run(debug=True)
