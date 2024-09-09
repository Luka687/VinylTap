import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5000/api'; // Flask API URL
  private token: string | null = null;
  private isAdmin: boolean = false; // Renamed from isAdmin

  constructor(private http: HttpClient, private router: Router) {}

  // Login method using query parameters
  login(username: string, password: string) {
    const params = new HttpParams().set('username', username).set('password', password);
    this.http.get<{ token: string, is_admin: boolean }>(`${this.apiUrl}/login`, { params })
      .subscribe(response => {
        this.token = response.token;
        this.isAdmin = response.is_admin; // Updated variable name
        localStorage.setItem('token', this.token);
        localStorage.setItem('userIsAdmin', JSON.stringify(this.isAdmin)); // Updated key name
        this.router.navigate(['/']);
      });
  }

  register(username: string, password: string): Observable<any> {
    const params = new HttpParams().set('username', username).set('password', password);
    return this.http.post<{ success: boolean }>(`${this.apiUrl}/register`, params);
  }

  // Check if user is logged in
  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  // Get user admin status
  getUserIsAdmin(): boolean { // Renamed method
    return JSON.parse(localStorage.getItem('userIsAdmin') || 'false'); // Updated key name
  }

  // Logout method
  logout() {
    this.token = null;
    this.isAdmin = false; // Updated variable name
    localStorage.removeItem('token');
    localStorage.removeItem('userIsAdmin'); // Updated key name
    this.router.navigate(['/login']);
  }
}