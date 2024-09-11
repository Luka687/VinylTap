import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
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

    // Method to create a new record
    createRecord(name: string, year: number, genre: string, artist: string, img_link:string){
      return this.http.post<{ success: boolean }>(`${this.apiUrl}?name=${name}&genre=${genre}&year_of_release=${year}&artist=${artist}&img_link=${img_link}`, null, {
        headers: new HttpHeaders({
          'Authorization': `${localStorage.getItem('token')}`
        })
      }).subscribe({
        next: (response) => {
          console.log('Post successful:', response);
        },
        error: (error) => {
          console.error('Post failed:', error);
        }
      });
  }
  
    // Method to update an existing record
    updateRecord(id: number, name: string, year: number, genre: string, artist: string, img_link:string){
      return this.http.patch<{ success: boolean }>(`${this.apiUrl}/${id}?name=${name}&genre=${genre}&year_of_release=${year}&artist=${artist}&img_link=${img_link}`, null, {
        headers: new HttpHeaders({
          'Authorization': `${localStorage.getItem('token')}`
        })
      }).subscribe({
        next: (response) => {
          console.log('Patch successful:', response);
        },
        error: (error) => {
          console.error('Patch failed:', error);
        }
      });
    }

    deleteRecord(id: number){
      // Construct the URL with the record ID
      const url = `${this.apiUrl}/${id}`;

      return this.http.delete<{ success: boolean }>(url, {
        headers: new HttpHeaders({
          'Authorization': `${localStorage.getItem('token')}`
        })
      }).subscribe({
        next: (response) => {
          console.log('Patch successful:', response);
        },
        error: (error) => {
          console.error('Patch failed:', error);
        }
      });;
    }

}
