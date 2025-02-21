import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  urlApi:string = "http://localhost:5000/"

  getPlaylistOrAlbumInfo(spotifyLink:string){
    return this.http.get(this.urlApi+"getPlaylistOrAlbumInfo?spotifyLink="+spotifyLink)
  }
  downloadOneTrack(youtubeCode:string){
    return this.http.get(this.urlApi+"/downloadOneTrack?youtubeCode="+youtubeCode,{headers: new HttpHeaders(),responseType: 'blob'})
  }
  downloadSpotifyAlbumOrPlaylist(spotifyLink:string){
    return this.http.get(this.urlApi+"/downloadSpotifyAlbumOrPlaylist?spotifyLink="+spotifyLink,{headers: new HttpHeaders(),responseType: 'blob'})
  }
  getTrackInfo(spotifyLink:string){
    return this.http.get(this.urlApi+"/getTrackInfo?spotifyLink="+spotifyLink)
  }


  constructor(private http:HttpClient) { }

}
