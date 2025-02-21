import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-home',
  standalone: false,
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  visibility:any={
    selectionVisibility:true,
    playlistVisibiliy:false,
    singleTrackVisibility:false
  }
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ){}
  sendButtonColor:string = ""
  sendButtonDisabled:boolean = false
  link = ""
  isLinkInputVisibile:boolean = false;
  params:any = {
    sito:"",
    type:""
  }
  linkInfo:any;

  isButtonSelected(sito:string,type:string){
    // console.log(this.params)
    if(sito == this.params.sito && type == this.params.type){
      return "1.05"
    }else{
      return "1.00"
    }
  }

  sendInfo(){
    console.log(this.params)
    if(this.params.type == "playlist" && this.params.sito == "spotify"){
      this.apiService.getPlaylistOrAlbumInfo(this.link).subscribe({
        next: (data:any) => {
          this.linkInfo = data
          this.visibility.selectionVisibility = false;
          this.visibility.playlistVisibiliy = true;
        }
      })
    }
    if(this.params.type == "track" && this.params.sito == "spotify"){
      this.apiService.getTrackInfo(this.link).subscribe({
        next: (data:any) => {
          this.linkInfo = data
          this.visibility.selectionVisibility = false;
          this.visibility.singleTrackVisibility = true;
        }
      })
    }
    if(this.params.type == "playlist" && this.params.sito == "youtube"){
      alert("Non implementato")
    }
    if(this.params.type == "track" && this.params.sito == "youtube"){
      alert("Non implementato")
    }

  }

  downloadOneTrack(item:any){
    this.apiService.downloadOneTrack(item.youtubeLink.split("=")[1].split("&")[0]).subscribe(response =>{
      const fileUrl = URL.createObjectURL(response);
      const a = document.createElement('a');
      a.href = fileUrl;
      a.download = item.artista+" - "+ item.titolo +".mp3";
      a.click();
      URL.revokeObjectURL(fileUrl);
    })
  }

  downloadAllTracks(){
    this.linkInfo.tracks.forEach((item:any) => {
      this.downloadOneTrack(item)
    });
  }
  downloadAllTracksZip(){
    this.apiService.downloadSpotifyAlbumOrPlaylist(this.link).subscribe(response =>{
      const fileUrl = URL.createObjectURL(response);
      const a = document.createElement('a');
      a.href = fileUrl;
      a.download = this.linkInfo.artista+" - "+ this.linkInfo.nome +".zip";
      a.click();
      URL.revokeObjectURL(fileUrl);
    })
  }

  backToSelection(){
    this.linkInfo = null;
    this.visibility.selectionVisibility = true;
    this.visibility.singleTrackVisibility = false;
    this.visibility.playlistVisibiliy = false;
  }

  changeLinkInputVisibility(sito:string,type:string){
    if(sito == "spotify"){
      this.sendButtonColor = "#1DB954"
    }
    if(sito == "youtube"){
      this.sendButtonColor =  "#f03"
    }
    this.params.sito = sito
    this.params.type = type
    if(!this.isLinkInputVisibile){
      this.isLinkInputVisibile = true;
    }
  }

  getTypeOfLink(){
    var res = null;
    if(this.link.includes("track")){
      res = "track"
    }
    if(this.link.includes("playlist") || this.link.includes("album")){
      res = "playlist"
    }
    if(res != this.params.type){
      this.sendButtonDisabled = true
    }else{
      this.sendButtonDisabled = false
    }
    return res
  }

}
