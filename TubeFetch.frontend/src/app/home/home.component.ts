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

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ){}
  sendButtonColor:string = ""
  link = ""
  isLinkInputVisibile:boolean = false;

  sendInfo(){
    console.log(this.link)
    this.apiService.getPlaylistOrAlbumInfo(this.link).subscribe(()=>{

    })
  }

  changeLinkInputVisibility(type:string){
    if(type == "spotify"){
      this.sendButtonColor = "#1DB954"
    }
    if(type == "youtube"){
      this.sendButtonColor =  "#f03"
    }
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        type: type
      },
      queryParamsHandling: 'replace',
    });
    this.isLinkInputVisibile = !this.isLinkInputVisibile
  }


}
