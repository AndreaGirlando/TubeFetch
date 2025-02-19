import os
import zipfile


def zipAlbumOrPlaylist(uniqueId):
    with zipfile.ZipFile(f"songs/{uniqueId}.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(f"songs/{uniqueId}"):
            for file in files:
                file_path = os.path.join(root, file)
                zf.write(file_path, os.path.relpath(file_path, f"songs/{uniqueId}"))
    return