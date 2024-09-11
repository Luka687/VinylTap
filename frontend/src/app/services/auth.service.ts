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
  private isAdmin: boolean = false;
  private user_id: number = 0;


  constructor(private http: HttpClient, private router: Router) {
    if(localStorage.getItem('userIsAdmin') == undefined){
      localStorage.setItem('userIsAdmin', JSON.stringify(this.isAdmin));
    }  
  }

  login(username: string, password: string) {
    const params = new HttpParams()
    .set('username', username)
    .set('password', password);
    
    this.http.get<{ token: string, is_admin: boolean, user_id: number }>(`${this.apiUrl}/login`, { params })
      .subscribe(response => {
        this.token = response.token;
        this.isAdmin = response.is_admin;
        this.user_id = response.user_id;
        localStorage.setItem('token', this.token);
        localStorage.setItem('userIsAdmin', JSON.stringify(this.isAdmin));
        localStorage.setItem('user_id', JSON.stringify(this.user_id));
        this.router.navigate(['/']);
      });
  }

  register(username: string, password: string){
    const params = new HttpParams()
      .set('username', username)
      .set('password', password);
    
    this.http.post<{ success: boolean }>(`${this.apiUrl}/register`, null, { params })
      .subscribe({
        next: (response) => {
          console.log('Registration successful:', response);
        },
        error: (error) => {
          console.error('Registration failed:', error);
        }
      });
  }

  // Check if user is logged in
  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  // Get user admin status
  getUserIsAdmin(): boolean {
    return JSON.parse(localStorage.getItem('userIsAdmin') || 'false');
  }

  // Logout method
  logout() {
    this.token = null;
    this.isAdmin = false;
    localStorage.removeItem('token');
    localStorage.removeItem('userIsAdmin');
    localStorage.removeItem('user_id');
    this.router.navigate(['/']);
  }
}