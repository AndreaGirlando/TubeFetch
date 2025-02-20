import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  urlApi:string = "http://localhost:5000/"

  getPlaylistOrAlbumInfo(spotifyLink:string){
    return this.http.get(this.urlApi+"getPlaylistOrAlbumInfo?spotifyLink="+spotifyLink)
  }

  constructor(private http:HttpClient) { }

}
