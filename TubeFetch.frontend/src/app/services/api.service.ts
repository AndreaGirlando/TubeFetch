import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  urlApi:string = "http://localhost:5000/"

  getSpotifyPlaylistOrAlbumInfo(spotifyLink:string){
    return this.http.get(this.urlApi+"getSpotifyPlaylistOrAlbumInfo?spotifyLink="+spotifyLink)
  }
  getYoutubePlaylistOrAlbumInfo(youtubeLink:string){
    return this.http.get(this.urlApi+"getYoutubePlaylistOrAlbumInfo?youtubeLink="+youtubeLink)
  }
  downloadSpotifyAlbumOrPlaylist(spotifyLink:string){
    return this.http.get(this.urlApi+"downloadSpotifyAlbumOrPlaylist?spotifyLink="+spotifyLink,{headers: new HttpHeaders(),responseType: 'blob'})
  }
  downloadYoutubeAlbumOrPlaylist(youtubeLink:string){
    return this.http.get(this.urlApi+"downloadYoutubeAlbumOrPlaylist?youtubeLink="+youtubeLink,{headers: new HttpHeaders(),responseType: 'blob'})
  }
  getSpotifyTrackInfo(spotifyLink:string){
    return this.http.get(this.urlApi+"getSpotifyTrackInfo?spotifyLink="+spotifyLink)
  }
  getYoutubeTrackInfo(youtubeLink:string){
    return this.http.get(this.urlApi+"getYoutubeTrackInfo?youtubeLink="+youtubeLink)
  }

  downloadOneTrack(youtubeCode:string){
    return this.http.get(this.urlApi+"downloadOneTrack?youtubeCode="+youtubeCode,{headers: new HttpHeaders(),responseType: 'blob'})
  }

  constructor(private http:HttpClient) { }

}
