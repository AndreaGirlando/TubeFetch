import os
import re
import yt_dlp

def download_mp3(link, request_id):
    output_path = f'./songs/{request_id}/%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio',
        'extractaudio': True,
        'outtmpl': os.path.normpath(output_path),
        "windowsfilenames": True,
        "restrictfilenames": True,
        'noplaylist': True,
        'postprocessors': [{  # Post-process to convert to MP3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert to mp3
            'preferredquality': '0',  # '0' means best quality, auto-determined by source
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            title = info_dict["requested_downloads"][0]["filename"].split("\\")[-1].split(".webm")[0]
            return title

    except Exception as e:
        raise e
