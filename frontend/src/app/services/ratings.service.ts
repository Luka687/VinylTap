import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, map , of, catchError} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RatingsService {

  private apiUrl = 'http://localhost:5000/api/ratings';

  constructor(private http: HttpClient) {}

  getRatingExists(userId: number, recordId: number): Observable<boolean> {
    return this.http.get<any>(`${this.apiUrl}/${userId}/${recordId}`).pipe(
      map(response => true),
      catchError((error: HttpErrorResponse) => {
        if (error.status === 404) {
        }
        console.error('An unexpected error occurred:', error);
        return of(false);
      })
    );
  }

  // Create a new rating
  createRating(userId: number, recordId: number, rating: number){
    const apiKey = localStorage.getItem('token');

    let headers = new HttpHeaders();
    if (apiKey) {
      headers = new HttpHeaders({
        'Authorization': `${apiKey}`
      });
    }

    return this.http.post<{ success: boolean }>(`${this.apiUrl}/${userId}/${recordId}?rating=${rating}`, null, {headers}).subscribe({
      next: (response) => {
        console.log('Post successful:', response);
      },
      error: (error) => {
        console.error('Post failed:', error);
      }
    });
  }

  // Edit an existing rating
  editRating(userId: number, recordId: number, rating: number){
    const apiKey = localStorage.getItem('token');

    let headers = new HttpHeaders();
    if (apiKey) {
      headers = new HttpHeaders({
        'Authorization': `${apiKey}`
      });
    }
    const url = `${this.apiUrl}/${userId}/${recordId}?rating=${rating}`;
    return this.http.patch<any>(url, null, {headers}).subscribe({
      next: (response) => {
        console.log('Patch successful:', response);
      },
      error: (error) => {
        console.error('Patch failed:', error);
      }
    });;
  }
}
