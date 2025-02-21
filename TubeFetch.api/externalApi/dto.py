import json


class TrackDTO:
    def __init__(self, id: str, artista: str, titolo: str, numeroTraccia: int, youtubeLink: str, disco: str, copertina:str):
        self.id = id
        self.artista = artista
        self.titolo = titolo
        self.numeroTraccia = numeroTraccia
        self.youtubeLink = youtubeLink
        self.disco = disco
        self.copertina = copertina
    def __str__(self):
        return f"Track {self.disco}-{self.numeroTraccia}: {self.artista} - {self.titolo} (ID: {self.id}, YouTube: {self.youtubeLink})"
    def toJson(self):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4)

class AlbumOrPlaylistInfoDTO:
    def __init__(self, copertina: str, nome: str, dataRilascio: str, artista: str,tipo: str, tracks: list[TrackDTO]):
        self.copertina = copertina
        self.nome = nome
        self.dataRilascio = dataRilascio
        self.artista = artista
        self.tipo = tipo
        self.tracks = tracks

    def __str__(self):
        return f"{self.tipo}: {self.nome} - {self.artista} (Rilasciato: {self.dataRilascio}, Copertina: {self.copertina}), lista delle canzoni: {self.tracks}"

    def toJson(self):
        serialized_tracks = [json.loads(track.toJson()) for track in self.tracks]
        album_dict = self.__dict__.copy()
        album_dict['tracks'] = serialized_tracks
        return json.dumps(album_dict, ensure_ascii=False, indent=4)