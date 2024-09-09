import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RecordsService {
  private apiUrl = 'http://localhost:5000/api/records';

  constructor(private http: HttpClient) { }

  getRecords(): Observable<any[]> {
    return this.http.get<any>(this.apiUrl).pipe(
      map(response =>response.records)
    );
  }

  getRecordByID(id:number): Observable<any>{
    return this.http.get<any>(this.apiUrl + '/' + id).pipe(
      map(response =>{
        return{
          "id": response.id,
          "name": response.name, 
          "genre": response.genre,
          "artist": response.artist,
          "year_of_release": response.year_of_release,
          "rating": response.rating,
          "img_link": response.img_link
        }
      })
    );
  }
}
