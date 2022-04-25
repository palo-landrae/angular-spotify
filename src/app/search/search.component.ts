import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { SpotifyService } from '../spotify.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
})
export class SearchComponent {
  query: string;
  obsTrack: Observable<Object>;
  results: any;
  // faccio iniettare lo spotify service e faccio una ricerca
  constructor(private spotify: SpotifyService, private router: Router) {}

  submit(query: HTMLInputElement): void {
    if (!query.value) {
      return;
    }
    this.query = query.value;
    this.obsTrack = this.spotify.searchTrack(this.query);
    this.obsTrack.subscribe((data) => {
      this.results = data;
      console.log(this.results);
    });
  }

  goToTrack(id: string): void {
    this.router.navigateByUrl(`/track/${id}`);
  }

  renderResults(res: any): void {
    this.results = null;
    if (res && res.tracks && res.tracks.items) {
      this.results = res.tracks.items;
    }
  }
}
