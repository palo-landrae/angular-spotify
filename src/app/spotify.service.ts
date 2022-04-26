import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { environment } from "../environments/environment";

@Injectable({
  providedIn: "root",
})
export class SpotifyService {
  domain: string = environment.domain;

  constructor(private http: HttpClient) { }

  searchTrack(query: string) {
    const url = `${this.domain}/api/search_track?q=${query}&type=track`;
    return this.http.get(url);
  }

  getTrack(id: string) {
    const url = `${this.domain}/api/get_track?id=${id}`;
    return this.http.get(url);
  }
}
