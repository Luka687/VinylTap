import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service'; // Adjust the path as necessary
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  imports: [
    CommonModule,
    IonicModule,
    FormsModule
  ]
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  isLoginMode: boolean = true; // Toggle between login and registration

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {
    if (this.isLoginMode) {
      this.authService.login(this.username, this.password);
    } else {
      this.authService.register(this.username, this.password);
    }
  }

  switchMode() {
    this.isLoginMode = !this.isLoginMode;
  }
}