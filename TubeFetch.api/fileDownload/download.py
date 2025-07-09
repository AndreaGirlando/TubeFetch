import os
import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import requests
import re
from externalApi.dto import TrackDTO
from externalApi.spotify import fromIdGetMetadata

def pulisci_titolo(titolo_completo):
    titolo_pulito = re.sub(r"[\[\(].*?[\]\)]", "", titolo_completo)
    if " - " in titolo_pulito:
        titolo, artista = titolo_pulito.split(" - ", 1)
    else:
        titolo = titolo_pulito
        artista = None
    return titolo.strip(), artista.strip() if artista else None

def download_mp3(track:TrackDTO, uniqueId = 0):
    if(uniqueId == 0): uniqueId = track.id
    folder = f'./songs/{uniqueId}'
    os.makedirs(folder, exist_ok=True)

    output_template = os.path.normpath(f'{folder}/%(title)s.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': output_template,
        'restrictfilenames': True,
        'windowsfilenames': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
        'prefer_ffmpeg': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(track.youtubeLink, download=True)

            # Accesso sicuro al filename
            filename = info.get('_filename')
            if not filename:
                downloads = info.get("requested_downloads", [])
                if not downloads:
                    raise ValueError("Impossibile determinare il percorso del file scaricato.")
                filename = downloads[0].get("filepath")
            if not filename:
                raise ValueError("Il filename finale è ancora indefinito.")

            metadata = fromIdGetMetadata(uniqueId)

            if metadata != []:

                audio = EasyID3(filename)
                audio['title'] = metadata["title"]
                audio['artist'] = metadata["artist"]
                audio['album'] = metadata["albumName"]
                audio['tracknumber'] = str(metadata["trackNumber"])
                audio['albumartist'] = metadata["albumArtist"]
                audio['date'] = metadata["dataRilascio"]
                audio['website'] = metadata["website"]
                audio.save()

                # Scrittura immagine di copertina
                if metadata["coverUrl"]:
                    file = MP3(filename, ID3=ID3)
                    try:
                        file.add_tags()
                    except Exception:
                        pass
                    image_data = requests.get(metadata["coverUrl"]).content
                    file.tags.add(APIC(
                        encoding=0,
                        mime='image/jpeg',
                        type=3,  # cover front
                        desc='Cover',
                        data=image_data
                    ))
                    file.save(v2_version=3)

            return {
                "filename": filename,
                "title": info.get("title", "")
            }
    except Exception as e:
        print("Errore:", e)
        raise