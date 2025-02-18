import json


class PlaylistTracksDTO:
    def __init__(self, id: str, artista: str, canzone: str, numeroTraccia: int, youtubeLink: str, disco: str):
        self.id = id
        self.artista = artista
        self.canzone = canzone
        self.numeroTraccia = numeroTraccia
        self.youtubeLink = youtubeLink
        self.disco = disco
    def __str__(self):
        return f"Track {self.disco}-{self.numeroTraccia}: {self.artista} - {self.canzone} (ID: {self.id}, YouTube: {self.youtubeLink})"

class AlbumOrPlaylistInfoDTO:
    def __init__(self, copertina: str, nome: str, dataRilascio: str, artista: str,tipo: str):
        self.copertina = copertina
        self.nome = nome
        self.dataRilascio = dataRilascio
        self.artista = artista
        self.tipo = tipo

    def __str__(self):
        return f"{self.tipo}: {self.nome} - {self.artista} (Rilasciato: {self.dataRilascio}, Copertina: {self.copertina})"

    def toJson(self):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4)